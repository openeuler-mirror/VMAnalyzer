#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""String sanitization helpers for safe display and storage."""

import re

_CONTROL_RE = re.compile(r"[\x00-\x1f\x7f]")


def sanitize_name(name, replacement="_"):
    """Strip control chars and trim a VM/domain name for display."""
    if name is None:
        return ""
    cleaned = _CONTROL_RE.sub(replacement, str(name))
    return cleaned.strip()[:255]


def sanitize_for_console(value, width=None):
    """Make a value safe for single-line console output."""
    text = "" if value is None else str(value)
    text = _CONTROL_RE.sub(" ", text).replace("\n", " ").replace("\r", " ")
    text = " ".join(text.split())
    if width and len(text) > width:
        text = text[:width - 1] + "~"
    return text


def sanitize_label(label):
    """Return a label suitable for use as a report column header."""
    cleaned = sanitize_name(label)
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", cleaned)
    return cleaned.strip("_").lower()
