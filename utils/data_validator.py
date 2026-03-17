#!/usr/bin/env python
# _*_coding: utf-8 _*_
"""数据验证工具"""
def validate_cpu_usage(value):
    return 0 <= value <= 100
def validate_memory_usage(value):
    return 0 <= value <= 100
def validate_positive_int(value):
    return isinstance(value, int) and value >= 0
