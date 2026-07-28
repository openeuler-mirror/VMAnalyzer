#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Outlier detection helpers based on the interquartile range."""


def _percentile(values, pct):
    """Return the pct-th percentile (0..100) using linear interpolation."""
    if not values:
        return 0.0
    ordered = sorted(float(v) for v in values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (pct / 100.0) * (len(ordered) - 1)
    low = int(rank)
    high = min(low + 1, len(ordered) - 1)
    frac = rank - low
    return ordered[low] * (1 - frac) + ordered[high] * frac


def _quartiles(values):
    """Return (q1, q2, q3) for a list of values."""
    return (_percentile(values, 25), _percentile(values, 50), _percentile(values, 75))


def detect_outliers(values, factor=1.5):
    """Return values that fall outside the IQR fences."""
    if not values or len(values) < 4:
        return []
    q1, _, q3 = _quartiles(values)
    iqr = q3 - q1
    low_fence = q1 - factor * iqr
    high_fence = q3 + factor * iqr
    return [v for v in values if v < low_fence or v > high_fence]


def is_outlier(value, values, factor=1.5):
    """Return True when value lies outside the IQR fences of values."""
    if not values or len(values) < 4:
        return False
    q1, _, q3 = _quartiles(values)
    iqr = q3 - q1
    low_fence = q1 - factor * iqr
    high_fence = q3 + factor * iqr
    return value < low_fence or value > high_fence


def remove_outliers(values, factor=1.5):
    """Return a new list with outlier values removed."""
    if not values or len(values) < 4:
        return list(values)
    q1, _, q3 = _quartiles(values)
    iqr = q3 - q1
    low_fence = q1 - factor * iqr
    high_fence = q3 + factor * iqr
    return [v for v in values if low_fence <= v <= high_fence]
