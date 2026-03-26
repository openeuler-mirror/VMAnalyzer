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
CSV Export Module for VMAnalyzer

This module provides functionality to export VM metrics data to CSV format,
making it easy to analyze data in spreadsheet applications.
"""
import csv
import json
import os
import time
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CSVExporter:
    """
    Export VM metrics data to CSV format.
    """
    
    def __init__(self, output_dir='./exports'):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def export_from_redis(self, redis_client, vm_uuid=None, start_time=None, 
                          end_time=None, output_file=None):
        """
        Export metrics from Redis to CSV.
        
        Args:
            redis_client: Redis client instance
            vm_uuid: Specific VM UUID to export (None for all VMs)
            start_time: Start timestamp (None for no limit)
            end_time: End timestamp (None for no limit)
            output_file: Output CSV file path (None for auto-generated)
            
        Returns:
            str: Path to the exported CSV file
        """
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = os.path.join(self.output_dir, f'vm_metrics_{timestamp}.csv')
        
        # Get data from Redis
        pattern = f'vm:{vm_uuid}:*' if vm_uuid else 'vm:*'
        keys = redis_client.keys(pattern)
        
        if not keys:
            logger.warning("No data found matching the criteria")
            return None
        
        # Collect all metrics
        all_metrics = []
        for key in keys:
            try:
                data = redis_client.get(key)
                if data:
                    metrics = json.loads(data)
                    metrics['_key'] = key.decode() if isinstance(key, bytes) else key
                    all_metrics.append(metrics)
            except Exception as e:
                logger.error(f"Error processing key {key}: {e}")
        
        # Sort by timestamp if available
        all_metrics.sort(key=lambda x: x.get('timestamp', 0))
        
        # Write to CSV
        if all_metrics:
            self._write_csv(all_metrics, output_file)
            logger.info(f"Exported {len(all_metrics)} records to {output_file}")
            return output_file
        
        return None
    
    def _write_csv(self, metrics_list, output_file):
        """Write metrics list to CSV file."""
        if not metrics_list:
            return
        
        # Get all possible fields
        fieldnames = set()
        for metrics in metrics_list:
            fieldnames.update(metrics.keys())
        
        # Prioritize common fields
        prioritized_fields = ['timestamp', 'vm_name', 'vm_uuid', 'cpu_usage', 
                             'memory_usage', 'memory_total', 'memory_available']
        fieldnames = prioritized_fields + sorted(fieldnames - set(prioritized_fields))
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(metrics_list)
    
    def export_summary(self, redis_client, output_file=None):
        """
        Export a summary report with aggregated statistics.
        
        Args:
            redis_client: Redis client instance
            output_file: Output CSV file path
            
        Returns:
            str: Path to the exported CSV file
        """
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = os.path.join(self.output_dir, f'vm_summary_{timestamp}.csv')
        
        keys = redis_client.keys('vm:*')
        
        # Aggregate by VM
        vm_stats = {}
        for key in keys:
            try:
                data = redis_client.get(key)
                if data:
                    metrics = json.loads(data)
                    vm_uuid = metrics.get('vm_uuid', 'unknown')
                    
                    if vm_uuid not in vm_stats:
                        vm_stats[vm_uuid] = {
                            'vm_name': metrics.get('vm_name', 'unknown'),
                            'count': 0,
                            'cpu_usage_sum': 0,
                            'memory_usage_sum': 0,
                            'max_cpu': 0,
                            'max_memory': 0
                        }
                    
                    stats = vm_stats[vm_uuid]
                    stats['count'] += 1
                    
                    cpu = metrics.get('cpu_usage', 0)
                    memory = metrics.get('memory_usage', 0)
                    
                    stats['cpu_usage_sum'] += cpu
                    stats['memory_usage_sum'] += memory
                    stats['max_cpu'] = max(stats['max_cpu'], cpu)
                    stats['max_memory'] = max(stats['max_memory'], memory)
            
            except Exception as e:
                logger.error(f"Error processing key {key}: {e}")
        
        # Calculate averages and prepare output
        summary_data = []
        for vm_uuid, stats in vm_stats.items():
            summary_data.append({
                'vm_uuid': vm_uuid,
                'vm_name': stats['vm_name'],
                'sample_count': stats['count'],
                'avg_cpu_usage': round(stats['cpu_usage_sum'] / stats['count'], 2) if stats['count'] > 0 else 0,
                'avg_memory_usage': round(stats['memory_usage_sum'] / stats['count'], 2) if stats['count'] > 0 else 0,
                'max_cpu_usage': stats['max_cpu'],
                'max_memory_usage': stats['max_memory']
            })
        
        # Write summary CSV
        if summary_data:
            fieldnames = ['vm_uuid', 'vm_name', 'sample_count', 'avg_cpu_usage',
                         'avg_memory_usage', 'max_cpu_usage', 'max_memory_usage']
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(summary_data)
            
            logger.info(f"Exported summary for {len(summary_data)} VMs to {output_file}")
            return output_file
        
        return None


def export_to_csv_command(args):
    """
    Command-line interface for CSV export.
    
    Usage:
        python -m utils.csv_export --summary
        python -m utils.csv_export --vm <uuid>
    """
    import argparse
    import redis
    
    parser = argparse.ArgumentParser(description='Export VMAnalyzer metrics to CSV')
    parser.add_argument('--redis-host', default='localhost', help='Redis host')
    parser.add_argument('--redis-port', type=int, default=6379, help='Redis port')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--summary', action='store_true', help='Export summary report')
    parser.add_argument('--vm', help='Export specific VM by UUID')
    parser.add_argument('--output-dir', default='./exports', help='Output directory')
    
    parsed_args = parser.parse_args(args)
    
    # Connect to Redis
    r = redis.Redis(host=parsed_args.redis_host, port=parsed_args.redis_port)
    
    exporter = CSVExporter(output_dir=parsed_args.output_dir)
    
    if parsed_args.summary:
        result = exporter.export_summary(r, parsed_args.output)
    else:
        result = exporter.export_from_redis(r, vm_uuid=parsed_args.vm, 
                                            output_file=parsed_args.output)
    
    if result:
        print(f"Successfully exported to: {result}")
    else:
        print("No data to export")


if __name__ == '__main__':
    import sys
    export_to_csv_command(sys.argv[1:])
