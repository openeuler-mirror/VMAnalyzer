#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Timestamp formatting and conversion helpers."""

import time

_DEFAULT_FMT = "%Y-%m-%d %H:%M:%S"


def format_timestamp(ts, fmt=_DEFAULT_FMT):
    """Format a unix epoch timestamp into a human readable string."""
    if ts is None:
        return ""
    try:
        return time.strftime(fmt, time.localtime(float(ts)))
    except (TypeError, ValueError):
        return ""


def parse_timestamp(text, fmt=_DEFAULT_FMT):
    """Parse a formatted timestamp string into a unix epoch value."""
    if not text:
        return None
    try:
        return time.mktime(time.strptime(str(text), fmt))
    except (TypeError, ValueError):
        return None


def to_iso(ts):
    """Return an ISO-8601 style string for a unix epoch timestamp."""
    if ts is None:
        return ""
    try:
        return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(float(ts)))
    except (TypeError, ValueError):
        return ""


def now():
    """Return the current unix epoch timestamp."""
    return time.time()
