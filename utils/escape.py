#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""String escape helpers for safe report output in multiple formats."""


def escape_csv(value):
    """Quote and escape a value for inclusion in a CSV field."""
    if value is None:
        return ""
    text = str(value)
    if "," in text or '"' in text or "\n" in text:
        text = '"' + text.replace('"', '""') + '"'
    return text


def escape_shell(value):
    """Escape a value for safe inclusion in a POSIX shell command."""
    if value is None:
        return "''"
    text = str(value)
    return "'" + text.replace("'", "'\\''") + "'"


_ESCAPE_MAP = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
}


def escape_html(value):
    """Escape a value for safe inclusion in HTML output."""
    if value is None:
        return ""
    text = str(value)
    return "".join(_ESCAPE_MAP.get(ch, ch) for ch in text)


def truncate_escaped(value, limit):
    """Escape for HTML then truncate to a maximum length."""
    escaped = escape_html(value)
    if len(escaped) <= limit:
        return escaped
    return escaped[:limit - 1] + "~"
