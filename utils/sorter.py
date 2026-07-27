#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Sorting helpers for collections of stat dictionaries."""


def sort_by_key(stats, key, descending=False):
    """Sort a list of dicts by a given key, ignoring missing values."""
    def _key(item):
        value = item.get(key) if isinstance(item, dict) else None
        if value is None:
            return float("-inf") if descending else float("inf")
        return value
    return sorted(stats, key=_key, reverse=descending)


def sort_stats(stats, keys, descending=False):
    """Sort stats by multiple keys (e.g. ['name', 'cpu'])."""
    if not keys:
        return list(stats)
    def _key(item):
        result = []
        for key in keys:
            value = item.get(key) if isinstance(item, dict) else None
            result.append((value is None, value))
        return result
    return sorted(stats, key=_key, reverse=descending)


def unique_sorted(values):
    """Return a sorted list of unique values from an iterable."""
    return sorted(set(values))
