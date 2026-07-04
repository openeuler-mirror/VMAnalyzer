#!/usr/bin/env python
# _*_coding: utf-8 _*_
"""Documentation for this component."""
COLLECTION_CONFIG = {
    "default_interval": 60,
    "cpu_interval": 10,
    "memory_interval": 30,
    "disk_interval": 60,
    "network_interval": 10
}

# Metrics collection whitelist - only collect specified metrics
# Empty list means collect all metrics
METRICS_WHITELIST = [
    # "cpu_usage",
    # "memory_usage",
    # "disk_usage",
]

def is_metric_enabled(metric_name):
    """Check if metric is enabled for collection"""
    if not METRICS_WHITELIST:
        return True
    return metric_name in METRICS_WHITELIST
