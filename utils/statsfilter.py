#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Filtering helpers for collections of stat dictionaries."""


def filter_by_predicate(stats, predicate):
    """Return stats for which predicate(stat) is truthy."""
    return [s for s in stats if predicate(s)]


def filter_by_key_value(stats, key, value):
    """Return stats whose key equals the given value."""
    return [s for s in stats if isinstance(s, dict) and s.get(key) == value]


def filter_positive(stats, key):
    """Return stats where the value at key is greater than zero."""
    result = []
    for s in stats:
        if not isinstance(s, dict):
            continue
        value = s.get(key)
        if isinstance(value, (int, float)) and value > 0:
            result.append(s)
    return result


def filter_in_range(stats, key, low, high):
    """Return stats whose key value lies within [low, high]."""
    result = []
    for s in stats:
        if not isinstance(s, dict):
            continue
        value = s.get(key)
        if isinstance(value, (int, float)) and low <= value <= high:
            result.append(s)
    return result
