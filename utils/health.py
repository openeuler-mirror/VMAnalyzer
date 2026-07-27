#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""VM health scoring helper that turns metrics into a 0..100 score."""

HEALTHY = "healthy"
DEGRADED = "degraded"
UNHEALTHY = "unhealthy"


def compute_health_score(cpu_util=None, mem_util=None, drop_rate=None):
    """Return a 0..100 health score from normalized metric inputs.

    Each input is a 0..1 ratio. Missing inputs are ignored.
    """
    penalties = []
    if cpu_util is not None and cpu_util > 0.85:
        penalties.append((cpu_util - 0.85) * 100)
    if mem_util is not None and mem_util > 0.90:
        penalties.append((mem_util - 0.90) * 100)
    if drop_rate is not None:
        penalties.append(min(drop_rate * 200, 60))
    penalty = min(sum(penalties), 100)
    return max(0.0, 100.0 - penalty)


def classify(score):
    """Map a health score to a categorical status."""
    if score >= 80:
        return HEALTHY
    if score >= 50:
        return DEGRADED
    return UNHEALTHY


def health_status(cpu_util=None, mem_util=None, drop_rate=None):
    """Return the categorical status for the given metrics."""
    return classify(compute_health_score(cpu_util, mem_util, drop_rate))
