#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Rounding helpers that keep metric output stable and readable."""

import math


def round_value(value, digits=2):
    """Round a numeric value, returning 0.0 for None."""
    if value is None:
        return 0.0
    try:
        return round(float(value), digits)
    except (TypeError, ValueError):
        return 0.0


def round_dict(mapping, digits=2):
    """Return a copy of a dict with all numeric values rounded."""
    result = {}
    if not isinstance(mapping, dict):
        return result
    for key, value in mapping.items():
        if isinstance(value, (int, float)):
            result[key] = round_value(value, digits)
        else:
            result[key] = value
    return result


def significant_digits(value, count=3):
    """Round to a fixed number of significant digits."""
    if value is None or value == 0:
        return 0.0
    try:
        value = float(value)
    except (TypeError, ValueError):
        return 0.0
    magnitude = math.floor(math.log10(abs(value)))
    decimals = count - int(magnitude) - 1
    return round(value, decimals)
