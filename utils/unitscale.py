#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Value scaling helpers that pick a friendly display unit."""

_SCALE_STEPS = [
    (1e12, "T"),
    (1e9, "G"),
    (1e6, "M"),
    (1e3, "K"),
    (1.0, ""),
]


class ScaleResult(object):
    """The outcome of scaling a value into a friendly unit."""

    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __str__(self):
        return "%.2f%s" % (self.value, self.unit)

    def to_dict(self):
        return {"value": self.value, "unit": self.unit}


def pick_unit(value):
    """Return (divisor, unit) appropriate for the magnitude of value."""
    magnitude = abs(value or 0)
    for divisor, unit in _SCALE_STEPS:
        if magnitude >= divisor:
            return divisor, unit
    return 1.0, ""


def scale_value(value):
    """Scale a value into a ScaleResult with a friendly unit."""
    if value is None:
        return ScaleResult(0.0, "")
    divisor, unit = pick_unit(value)
    return ScaleResult(value / divisor, unit)


def scale_series(values):
    """Scale a list of values using a single shared unit."""
    if not values:
        return []
    peak = max(abs(v) for v in values if v is not None) if any(v is not None for v in values) else 0
    divisor, unit = pick_unit(peak)
    return [ScaleResult((v or 0) / divisor, unit) for v in values]
