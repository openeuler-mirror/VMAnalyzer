#!/usr/bin/env python3
"""Weak reference map for caching without preventing GC."""
import weakref
from typing import Any, Dict, Optional

class WeakRefMap:
    """A map that holds weak references to values."""

    def __init__(self):
        self._map: Dict[str, Any] = {}

    def put(self, key: str, value: Any) -> None:
        try:
            self._map[key] = weakref.ref(value)
        except TypeError:
            self._map[key] = value

    def get(self, key: str) -> Optional[Any]:
        ref = self._map.get(key)
        if ref is None:
            return None
        if callable(ref):
            obj = ref()
            if obj is None:
                del self._map[key]
            return obj
        return ref

    def contains(self, key: str) -> bool:
        return self.get(key) is not None

    def remove(self, key: str) -> bool:
        if key in self._map:
            del self._map[key]
            return True
        return False

    def purge(self) -> int:
        dead = [k for k, v in self._map.items() if callable(v) and v() is None]
        for k in dead:
            del self._map[k]
        return len(dead)
