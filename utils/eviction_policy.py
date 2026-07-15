#!/usr/bin/env python3
"""Pluggable cache eviction strategies for managed caches."""
from collections import OrderedDict
from typing import Any, Optional

class EvictionPolicy:
    """Base eviction policy interface."""

    def access(self, key: Any) -> None:
        pass

    def evict_candidate(self, cache: OrderedDict) -> Optional[Any]:
        raise NotImplementedError

class LRU_Eviction(EvictionPolicy):
    """Least Recently Used eviction."""
    def evict_candidate(self, cache: OrderedDict) -> Optional[Any]:
        if cache:
            return next(iter(cache))
        return None

class FIFO_Eviction(EvictionPolicy):
    """First In First Out eviction."""
    def evict_candidate(self, cache: OrderedDict) -> Optional[Any]:
        if cache:
            return next(iter(cache))
        return None

class LFU_Eviction(EvictionPolicy):
    """Least Frequently Used eviction."""
    def __init__(self):
        self._freq = {}

    def access(self, key: Any) -> None:
        self._freq[key] = self._freq.get(key, 0) + 1

    def evict_candidate(self, cache: OrderedDict) -> Optional[Any]:
        if not cache:
            return None
        return min(cache.keys(), key=lambda k: self._freq.get(k, 0))
