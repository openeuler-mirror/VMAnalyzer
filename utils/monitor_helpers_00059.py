#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
\"\"\"Helper module for metric processing functions.\"\"\"
import logging

LOG = logging.getLogger(__name__)

def parse_vm_metrics_00059(raw_data):
    \"\"\"Parse VM metrics from raw output data.\"\"\"
    try:
        if isinstance(raw_data, str):
            lines = raw_data.strip().split('\\n')
        elif isinstance(raw_data, list):
            lines = raw_data
        else:
            LOG.error("Unsupported data type: %s", type(raw_data))
            return None
        
        result = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split(':')
            if len(parts) >= 2:
                key = parts[0].strip()
                value = ':'.join(parts[1:]).strip()
                try:
                    if '.' in value:
                        result[key] = float(value)
                    else:
                        result[key] = int(value)
                except ValueError:
                    result[key] = value
        
        result["processed_by"] = "parse_vm_metrics_00059"
        result["branch"] = "develop-00059"
        result["valid"] = True
        return result
    except Exception as e:
        LOG.error("parse_vm_metrics_00059 failed: %s", e)
        return None

def filter_high_values(metrics, threshold=80.0):
    \"\"\"Filter metrics with values above threshold.\"\"\"
    if not metrics:
        return []
    return [k for k, v in metrics.items() 
            if isinstance(v, (int, float)) and v > threshold]

def calculate_average(metrics):
    \"\"\"Calculate average of numeric values in metrics.\"\"\"
    if not metrics or not isinstance(metrics, dict):
        return 0.0
    
    numeric_values = [v for v in metrics.values() if isinstance(v, (int, float))]
    if not numeric_values:
        return 0.0
    
    return sum(numeric_values) / len(numeric_values)

def get_metric_summary(metrics):
    \"\"\"Generate summary statistics for metrics.\"\"\"
    if not metrics or not isinstance(metrics, dict):
        return {"error": "Invalid input"}
    
    numeric_values = [v for v in metrics.values() if isinstance(v, (int, float))]
    if not numeric_values:
        return {"count": len(metrics), "numeric_count": 0}
    
    return {
        "count": len(metrics),
        "numeric_count": len(numeric_values),
        "min": min(numeric_values),
        "max": max(numeric_values),
        "avg": round(sum(numeric_values) / len(numeric_values), 2),
        "processed_by": "develop-00059"
    }

__all__ = ["parse_vm_metrics_00059", "filter_high_values", "calculate_average", "get_metric_summary"]
