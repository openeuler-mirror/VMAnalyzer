#!/usr/bin/env python
# _*_coding: utf-8 _*_
"""指标收集框架"""
class MetricsCollector:
    def __init__(self):
        self.metrics = []
    def add(self, name, value, labels=None):
        self.metrics.append({"name": name, "value": value, "labels": labels or {}})
    def get_all(self):
        return self.metrics
