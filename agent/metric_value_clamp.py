#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Clamp implausible metric values before they reach storage."""

import logging
import math

LOG = logging.getLogger(__name__)


def clamp(value, low=None, high=None, default=0.0):
    """Constrain *value* to the given range, replacing NaN with *default*."""
    if value is None:
        return default
    try:
        number = float(value)
    except (TypeError, ValueError):
        LOG.debug("non-numeric metric value %r", value)
        return default
    if math.isnan(number) or math.isinf(number):
        return default
    if low is not None and number < low:
        return low
    if high is not None and number > high:
        return high
    return number


def clamp_ratio(value, default=0.0):
    """Convenience clamp for ratios that must stay within 0..1."""
    return clamp(value, 0.0, 1.0, default)


def clamp_percent(value, default=0.0):
    """Convenience clamp for percentages within 0..100."""
    return clamp(value, 0.0, 100.0, default)
