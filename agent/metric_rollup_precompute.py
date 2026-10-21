#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Precompute coarse rollups from fine-grained metric series."""

import logging

LOG = logging.getLogger(__name__)

AGGREGATORS = {
    "avg": lambda values: sum(values) / len(values) if values else 0.0,
    "sum": sum,
    "max": max,
    "min": min,
}


def rollup(series, factor=4, aggregate="avg"):
    """Collapse consecutive runs of *factor* points into single values."""
    if factor <= 0:
        raise ValueError("factor must be positive")
    reducer = AGGREGATORS.get(aggregate)
    if reducer is None:
        raise ValueError("unsupported aggregate: {}".format(aggregate))
    values = list(series)
    result = []
    for start in range(0, len(values), factor):
        window = values[start:start + factor]
        if not window:
            continue
        result.append(reducer(window))
    LOG.debug("rolled %d points into %d buckets", len(values), len(result))
    return result


def rollup_map(series_map, factor=4, aggregate="avg"):
    """Apply the rollup to every series in a mapping."""
    return {
        name: rollup(series, factor, aggregate)
        for name, series in series_map.items()
    }
