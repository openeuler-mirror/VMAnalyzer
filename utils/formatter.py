#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Human-readable formatting helpers for metric values."""

_UNITS = ("B", "KiB", "MiB", "GiB", "TiB", "PiB")


def format_bytes(value, binary=True):
    """Return a human readable byte string such as '1.25 MiB'."""
    if value is None or value < 0:
        return "0 B"
    base = 1024 if binary else 1000
    size = float(value)
    for unit in _UNITS:
        if size < base:
            return "%.2f %s" % (size, unit)
        size /= base
    return "%.2f %s" % (size, _UNITS[-1])


def format_duration(seconds):
    """Return a compact duration string like '1h 02m 03s'."""
    if seconds is None or seconds < 0:
        return "0s"
    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    parts = []
    if hours:
        parts.append("%dh" % hours)
    if minutes or hours:
        parts.append("%02dm" % minutes)
    parts.append("%02ds" % secs)
    return " ".join(parts)


def format_count(value, suffix=""):
    """Format an integer count with thousands separators."""
    if value is None:
        return "0%s" % suffix
    return "{:,}{suffix}".format(int(value), suffix=suffix)


def format_percent(ratio, digits=2):
    """Format a 0..1 ratio as a percentage string."""
    if ratio is None:
        return "0.00%"
    return "%.*f%%" % (digits, ratio * 100)
