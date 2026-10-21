#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Distribute a cycle timeout across a series of collection tasks."""

import logging

LOG = logging.getLogger(__name__)


def allocate(total_seconds, weights, reserve=0.0):
    """Split *total_seconds* proportionally, keeping a reserve untouched."""
    usable = max(0.0, total_seconds - reserve)
    weights = [max(0.0, float(weight)) for weight in weights]
    total_weight = sum(weights)
    if total_weight <= 0:
        share = usable / len(weights) if weights else 0.0
        return [round(share, 3) for _ in weights]
    return [round(usable * weight / total_weight, 3) for weight in weights]


def remaining(total_seconds, elapsed, reserve=0.0):
    """Seconds left for the rest of the cycle."""
    return max(0.0, total_seconds - elapsed - reserve)


def expired(total_seconds, elapsed, reserve=0.0):
    """True when no time is left for further work."""
    return remaining(total_seconds, elapsed, reserve) <= 0.0
