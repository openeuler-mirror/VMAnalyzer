#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Percentile and quartile helpers for metric distributions."""


def percentile(values, pct):
    """Return the pct-th percentile (0..100) using nearest-rank method."""
    if not values:
        return 0.0
    if pct < 0 or pct > 100:
        raise ValueError("percentile must be between 0 and 100")
    ordered = sorted(float(v) for v in values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (pct / 100.0) * (len(ordered) - 1)
    low = int(rank)
    high = min(low + 1, len(ordered) - 1)
    frac = rank - low
    return ordered[low] * (1 - frac) + ordered[high] * frac


def median(values):
    """Return the median (50th percentile) of a list of values."""
    return percentile(values, 50)


def quartiles(values):
    """Return (q1, q2, q3) for a list of values."""
    return (percentile(values, 25), percentile(values, 50), percentile(values, 75))


def iqr(values):
    """Return the interquartile range of a list of values."""
    q1, _, q3 = quartiles(values)
    return q3 - q1
