#!/usr/bin/env python
# _*_coding: utf-8 _*_
#######################################################################################
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
#######################################################################################
"""
Metrics Aggregation Module for VMAnalyzer

This module provides aggregation functions for VM metrics data,
including statistical calculations like min, max, avg, percentiles.
"""
import statistics
from collections import defaultdict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class MetricsAggregator:
    """
    Aggregates VM metrics over time periods.
    """
    
    def __init__(self, storage):
        """
        Args:
            storage: VMStatsStorage instance
        """
        self.storage = storage
    
    def aggregate_by_vm(self, vm_uuid, metric_name, time_range_minutes=60):
        """
        Aggregate metrics for a specific VM.
        
        Args:
            vm_uuid: VM UUID
            metric_name: Name of the metric (e.g., 'cpu_usage')
            time_range_minutes: Time range to aggregate
            
        Returns:
            dict: Aggregation results
        """
        # Get historical data from storage
        metrics = self._get_metrics_history(vm_uuid, time_range_minutes)
        
        if not metrics:
            return None
        
        values = [m.get(metric_name, 0) for m in metrics if metric_name in m]
        
        if not values:
            return None
        
        return self._calculate_stats(values)
    
    def aggregate_all_vms(self, metric_name, time_range_minutes=60):
        """
        Aggregate metrics across all VMs.
        
        Args:
            metric_name: Name of the metric
            time_range_minutes: Time range to aggregate
            
        Returns:
            dict: Per-VM aggregation results
        """
        results = {}
        vms = self.storage.get_all_vm_uuids()
        
        for vm_uuid in vms:
            try:
                agg = self.aggregate_by_vm(vm_uuid, metric_name, time_range_minutes)
            except Exception as e:
                logger.warning("Failed to process VM %s: %s", vm_uuid, str(e))
                continue

            if agg:
                vm_name = self.storage.get_vm_name(vm_uuid)
                results[vm_uuid] = {
                    'name': vm_name,
                    'stats': agg
                }
        
        return results
    
    def _get_metrics_history(self, vm_uuid, time_range_minutes):
        """Get metrics history from storage."""
        # This is a placeholder - actual implementation depends on storage
        # Could query Redis with time-based keys or use a time-series DB
        return self.storage.get_metrics_history(vm_uuid, time_range_minutes)
    
    def _calculate_stats(self, values):
        """
        Calculate statistics for a list of values.
        
        Args:
            values: List of numeric values
            
        Returns:
            dict: Statistical measures
        """
        if not values:
            return None
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        
        stats = {
            'count': n,
            'min': min(values),
            'max': max(values),
            'avg': round(statistics.mean(values), 2),
            'sum': round(sum(values), 2)
        }
        
        # Calculate median
        if n > 0:
            stats['median'] = round(statistics.median(values), 2)
        
        # Calculate standard deviation
        if n > 1:
            try:
                stats['stddev'] = round(statistics.stdev(values), 2)
            except statistics.StatisticsError:
                stats['stddev'] = 0
        else:
            stats['stddev'] = 0
        
        # Calculate percentiles
        stats['p95'] = round(self._percentile(sorted_values, 95), 2)
        stats['p99'] = round(self._percentile(sorted_values, 99), 2)
        
        return stats
    
    def _percentile(self, sorted_values, p):
        """Calculate percentile from sorted values."""
        n = len(sorted_values)
        if n == 0:
            return 0
        
        k = (n - 1) * p / 100
        f = int(k)
        c = f + 1 if f + 1 < n else f
        
        if f == c:
            return sorted_values[f]
        
        return sorted_values[f] + (k - f) * (sorted_values[c] - sorted_values[f])
    
    def get_top_consumers(self, metric_name, time_range_minutes=60, top_n=5):
        """
        Get top N VMs by metric consumption.
        
        Args:
            metric_name: Metric to rank by
            time_range_minutes: Time range
            top_n: Number of top VMs to return
            
        Returns:
            list: Top N VMs with their stats
        """
        all_stats = self.aggregate_all_vms(metric_name, time_range_minutes)
        
        # Sort by average value
        sorted_vms = sorted(
            all_stats.items(),
            key=lambda x: x[1]['stats']['avg'],
            reverse=True
        )
        
        return [
            {
                'uuid': uuid,
                'name': data['name'],
                'avg': data['stats']['avg'],
                'max': data['stats']['max']
            }
            for uuid, data in sorted_vms[:top_n]
        ]
    
    def detect_anomalies(self, vm_uuid, metric_name, threshold_stddev=2):
        """
        Detect anomalous values using standard deviation method.
        
        Args:
            vm_uuid: VM UUID
            metric_name: Metric to analyze
            threshold_stddev: Number of standard deviations for anomaly
            
        Returns:
            list: Anomalous data points
        """
        metrics = self._get_metrics_history(vm_uuid, 60)  # Last hour
        
        if len(metrics) < 10:
            return []
        
        values = [m.get(metric_name, 0) for m in metrics if metric_name in m]
        
        if len(values) < 10:
            return []
        
        mean = statistics.mean(values)
        stddev = statistics.stdev(values) if len(values) > 1 else 0
        
        anomalies = []
        for m in metrics:
            value = m.get(metric_name)
            if value is None:
                continue
            
            z_score = abs(value - mean) / stddev if stddev > 0 else 0
            
            if z_score > threshold_stddev:
                anomalies.append({
                    'timestamp': m.get('timestamp'),
                    'value': value,
                    'z_score': round(z_score, 2),
                    'expected_range': (
                        round(mean - threshold_stddev * stddev, 2),
                        round(mean + threshold_stddev * stddev, 2)
                    )
                })
        
        return anomalies


class TimeSeriesAggregator:
    """
    Aggregates metrics into time-series buckets.
    """
    
    def __init__(self, storage):
        self.storage = storage
    
    def aggregate_by_time(self, vm_uuid, metric_name, bucket_minutes=5, 
                          time_range_hours=24):
        """
        Aggregate metrics into time buckets.
        
        Args:
            vm_uuid: VM UUID
            metric_name: Metric name
            bucket_minutes: Bucket size in minutes
            time_range_hours: Total time range in hours
            
        Returns:
            list: Time bucket aggregations
        """
        metrics = self.storage.get_metrics_history(vm_uuid, time_range_hours * 60)
        
        if not metrics:
            return []
        
        # Group by time bucket
        buckets = defaultdict(list)
        
        for m in metrics:
            timestamp = m.get('timestamp')
            value = m.get(metric_name)
            
            if timestamp is None or value is None:
                continue
            
            # Round to bucket
            bucket_time = self._round_to_bucket(timestamp, bucket_minutes * 60)
            buckets[bucket_time].append(value)
        
        # Calculate stats for each bucket
        results = []
        for bucket_time in sorted(buckets.keys()):
            values = buckets[bucket_time]
            stats = self._calculate_bucket_stats(values)
            stats['timestamp'] = bucket_time
            results.append(stats)
        
        return results
    
    def _round_to_bucket(self, timestamp, bucket_seconds):
        """Round timestamp to bucket boundary."""
        return (timestamp // bucket_seconds) * bucket_seconds
    
    def _calculate_bucket_stats(self, values):
        """Calculate stats for a bucket."""
        if not values:
            return {'count': 0}
        
        return {
            'count': len(values),
            'min': round(min(values), 2),
            'max': round(max(values), 2),
            'avg': round(sum(values) / len(values), 2)
        }
