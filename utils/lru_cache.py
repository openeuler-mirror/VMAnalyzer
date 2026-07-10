#!/usr/bin/env python3
"""LRU cache implementation using OrderedDict."""
from collections import OrderedDict
from typing import Any, Optional

class LRUCache:
    def __init__(self, capacity: int = 128):
        self._capacity = capacity
        self._cache = OrderedDict()

    def get(self, key: Any) -> Optional[Any]:
        if key not in self._cache:
            return None
        self._cache.move_to_end(key)
        return self._cache[key]

    def put(self, key: Any, value: Any) -> None:
        if key in self._cache:
            self._cache.move_to_end(key)
        elif len(self._cache) >= self._capacity:
            self._cache.popitem(last=False)
        self._cache[key] = value

    def remove(self, key: Any) -> bool:
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self) -> None:
        self._cache.clear()

    def size(self) -> int:
        return len(self._cache)

    def keys(self) -> list:
        return list(self._cache.keys())
