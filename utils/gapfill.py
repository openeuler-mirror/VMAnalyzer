#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Gap-filling helpers for time series with missing samples."""


def _clamp(value, low, high):
    """Restrict a value to the [low, high] range."""
    if value is None:
        return low
    if value < low:
        return low
    if value > high:
        return high
    return value


def fill_gaps(samples, value_key, time_key, interval, strategy="linear"):
    """Fill missing samples in a time series using interpolation."""
    if not samples or len(samples) < 2:
        return list(samples)
    ordered = sorted(samples, key=lambda s: s.get(time_key, 0))
    result = [ordered[0]]
    for i in range(1, len(ordered)):
        prev = ordered[i - 1]
        cur = ordered[i]
        prev_time = prev.get(time_key, 0)
        cur_time = cur.get(time_key, 0)
        step = prev_time + interval
        while step < cur_time:
            fraction = (step - prev_time) / float(cur_time - prev_time)
            prev_value = prev.get(value_key, 0)
            cur_value = cur.get(value_key, 0)
            fill_value = prev_value + (cur_value - prev_value) * fraction
            result.append({time_key: step, value_key: fill_value, "filled": True})
            step += interval
        result.append(cur)
    return result


def interpolate_missing(prev_value, cur_value, fraction):
    """Linear interpolation between two values."""
    fraction = _clamp(fraction, 0.0, 1.0)
    return prev_value + (cur_value - prev_value) * fraction
