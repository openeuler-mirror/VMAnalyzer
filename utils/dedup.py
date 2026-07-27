#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Deduplication helpers for stat entries that share a key."""


def dedup_by_key(stats, key):
    """Keep the first occurrence of each key value in a list of dicts."""
    seen = set()
    result = []
    for s in stats:
        if not isinstance(s, dict):
            continue
        value = s.get(key)
        if value in seen:
            continue
        seen.add(value)
        result.append(s)
    return result


def dedup_stats(stats, keys):
    """Deduplicate stats by a composite key made of several fields."""
    seen = set()
    result = []
    for s in stats:
        if not isinstance(s, dict):
            continue
        fingerprint = tuple(s.get(k) for k in keys)
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        result.append(s)
    return result


def count_duplicates(stats, key):
    """Return how many entries share a key value with an earlier entry."""
    seen = set()
    duplicates = 0
    for s in stats:
        if not isinstance(s, dict):
            continue
        value = s.get(key)
        if value in seen:
            duplicates += 1
        else:
            seen.add(value)
    return duplicates
