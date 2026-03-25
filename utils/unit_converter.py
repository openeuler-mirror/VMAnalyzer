#!/usr/bin/env python
# _*_coding: utf-8 _*_
"""单位转换工具"""
def bytes_to_mb(bytes_val):
    return bytes_val / (1024 * 1024)
def bytes_to_gb(bytes_val):
    return bytes_val / (1024 * 1024 * 1024)
def ns_to_ms(ns_val):
    return ns_val / 1e6
