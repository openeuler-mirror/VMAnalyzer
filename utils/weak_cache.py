#!/usr/bin/env python3
"""Cache with weak references allowing garbage collection."""
import weakref
from typing import Any, Optional

class WeakCache:
    """Cache that uses weak references so unused entries can be GC'd."""

    def __init__(self):
        self._store = {}

    def set(self, key: str, value: Any) -> None:
        """Store a value with weak reference."""
        try:
            self._store[key] = weakref.ref(value)
        except TypeError:
            self._store[key] = value

    def get(self, key: str) -> Optional[Any]:
        """Retrieve a value if still alive."""
        ref = self._store.get(key)
        if ref is None:
            return None
        if callable(ref) and not isinstance(ref, str):
            obj = ref()
            if obj is None:
                del self._store[key]
            return obj
        return ref

    def delete(self, key: str) -> bool:
        """Remove a key from cache."""
        if key in self._store:
            del self._store[key]
            return True
        return False

    def cleanup(self) -> int:
        """Remove dead references."""
        dead = [k for k, v in self._store.items()
                if callable(v) and not isinstance(v, str) and v() is None]
        for k in dead:
            del self._store[k]
        return len(dead)

    def size(self) -> int:
        """Return approximate cache size."""
        return len(self._store)
