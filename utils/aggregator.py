#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Time-window aggregation for collected stat samples."""


class WindowAggregator(object):
    """Group samples into fixed-size time windows and aggregate them."""

    def __init__(self, window_seconds, value_key, time_key):
        if window_seconds <= 0:
            raise ValueError("window_seconds must be positive")
        self.window_seconds = window_seconds
        self.value_key = value_key
        self.time_key = time_key

    def aggregate(self, samples):
        """Return a list of {window, count, avg} dicts."""
        buckets = {}
        for s in samples:
            if not isinstance(s, dict):
                continue
            ts = s.get(self.time_key)
            value = s.get(self.value_key)
            if ts is None or value is None:
                continue
            bucket = int(ts) // self.window_seconds
            buckets.setdefault(bucket, []).append(float(value))
        result = []
        for bucket in sorted(buckets):
            values = buckets[bucket]
            result.append({
                "window": bucket * self.window_seconds,
                "count": len(values),
                "avg": sum(values) / len(values),
            })
        return result


def aggregate_by_window(samples, window_seconds, value_key, time_key):
    """Functional helper wrapping WindowAggregator."""
    return WindowAggregator(window_seconds, value_key, time_key).aggregate(samples)
