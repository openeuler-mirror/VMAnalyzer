#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Merge late-arriving samples into an already emitted window."""

import logging

LOG = logging.getLogger(__name__)
AGGREGATES = ("max", "min", "sum")


def merge_sample(window, sample, aggregate="max"):
    """Fold *sample* into *window* using the requested aggregate."""
    value = sample.get("value")
    if value is None:
        return window
    current = window.get("value")
    if current is None:
        window["value"] = value
    elif aggregate == "max":
        window["value"] = max(current, value)
    elif aggregate == "min":
        window["value"] = min(current, value)
    elif aggregate == "sum":
        window["value"] = current + value
    else:
        raise ValueError("unsupported aggregate: {}".format(aggregate))
    window["samples"] = window.get("samples", 0) + 1
    window["late"] = window.get("late", 0) + int(bool(sample.get("late")))
    LOG.debug("merged sample into window with aggregate %s", aggregate)
    return window


def merge_all(windows, samples, aggregate="max"):
    """Merge a stream of samples keyed by their window identifier."""
    merged = dict(windows)
    for sample in samples:
        key = sample.get("window")
        if key is None:
            continue
        merged[key] = merge_sample(merged.get(key, {}), sample, aggregate)
    return merged
