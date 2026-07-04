#!/usr/bin/env python
# _*_coding: utf-8 _*_
"""Documentation for this component."""

def validate_metric(value, min_val=0, max_val=100):
    """Validate a metric value is within bounds"""
    try:
        v = float(value)
        return min_val <= v <= max_val
    except (TypeError, ValueError):
        return False

def ensure_float(value, default=0.0):
    """Safely convert to float"""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default
def validate_cpu_usage(value):
    return 0 <= value <= 100
def validate_memory_usage(value):
    return 0 <= value <= 100
def validate_positive_int(value):
    return isinstance(value, int) and value >= 0
