#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Comparison helpers that diff two stats snapshots."""


def compare_stats(prev, cur, keys=None):
    """Return a dict of {key: (prev, cur, delta)} for numeric keys."""
    if not isinstance(prev, dict) or not isinstance(cur, dict):
        return {}
    keys = keys or sorted(set(prev.keys()) | set(cur.keys))
    result = {}
    for key in keys:
        old = prev.get(key)
        new = cur.get(key)
        if isinstance(old, (int, float)) and isinstance(new, (int, float)):
            result[key] = (old, new, new - old)
    return result


def diff_snapshots(prev, cur, keys=None):
    """Return only the keys whose value changed between snapshots."""
    compared = compare_stats(prev, cur, keys)
    return {k: v for k, v in compared.items() if v[2] != 0}


def largest_changes(prev, cur, keys=None, count=3):
    """Return the top-n keys by absolute change magnitude."""
    compared = compare_stats(prev, cur, keys)
    ordered = sorted(compared.items(), key=lambda item: abs(item[1][2]), reverse=True)
    return ordered[:count]


def has_regression(prev, cur, key):
    """Return True when the value at key decreased between snapshots."""
    compared = compare_stats(prev, cur, [key])
    if key not in compared:
        return False
    return compared[key][2] < 0
