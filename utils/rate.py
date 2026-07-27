#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Rate-of-change computation helpers for metric series."""


def compute_rate(prev_value, cur_value, prev_time, cur_time):
    """Return the per-second rate of change between two samples."""
    if prev_time is None or cur_time is None:
        return 0.0
    delta_time = cur_time - prev_time
    if delta_time <= 0:
        return 0.0
    return (cur_value - prev_value) / float(delta_time)


def compute_rate_series(samples, value_key, time_key):
    """Yield (timestamp, rate) pairs for a list of sample dicts."""
    if not samples or len(samples) < 2:
        return
    prev = samples[0]
    for cur in samples[1:]:
        rate = compute_rate(prev.get(value_key, 0), cur.get(value_key, 0),
                            prev.get(time_key, 0), cur.get(time_key, 0))
        yield cur.get(time_key, 0), rate
        prev = cur


def average_rate(samples, value_key, time_key):
    """Return the average rate across a series of samples."""
    rates = [r for _, r in compute_rate_series(samples, value_key, time_key)]
    if not rates:
        return 0.0
    return sum(rates) / len(rates)
