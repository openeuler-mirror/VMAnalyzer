#!/usr/bin/env python3
"""Pre-allocated memory pool for object reuse to reduce allocation overhead."""
from typing import List, Any, Callable

class MemoryPool:
    """Manages a pool of pre-allocated objects for reuse."""

    def __init__(self, factory: Callable, size: int = 100):
        self._factory = factory
        self._pool: List[Any] = [factory() for _ in range(size)]
        self._in_use = set()

    def acquire(self) -> Any:
        """Get an object from the pool."""
        if not self._pool:
            obj = self._factory()
        else:
            obj = self._pool.pop()
        self._in_use.add(id(obj))
        return obj

    def release(self, obj: Any) -> None:
        """Return an object to the pool."""
        if id(obj) in self._in_use:
            self._in_use.discard(id(obj))
            self._pool.append(obj)

    def available(self) -> int:
        """Return count of available objects."""
        return len(self._pool)

    def in_use_count(self) -> int:
        """Return count of objects in use."""
        return len(self._in_use)

    def clear(self) -> None:
        """Clear the pool."""
        self._pool.clear()
        self._in_use.clear()
