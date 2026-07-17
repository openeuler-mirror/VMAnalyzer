#!/usr/bin/env python3
"""Generic resource pool management with checkout/checkin."""
import threading
from typing import Any, Callable, List

class ResourcePool:
    """Manages a pool of reusable resources with thread safety."""

    def __init__(self, factory: Callable[[], Any], size: int = 10):
        self._factory = factory
        self._available: List[Any] = [factory() for _ in range(size)]
        self._in_use: List[Any] = []
        self._lock = threading.Lock()

    def checkout(self) -> Any:
        """Check out a resource from the pool."""
        with self._lock:
            if self._available:
                res = self._available.pop()
                self._in_use.append(res)
                return res
            res = self._factory()
            self._in_use.append(res)
            return res

    def checkin(self, resource: Any) -> None:
        """Return a resource to the pool."""
        with self._lock:
            if resource in self._in_use:
                self._in_use.remove(resource)
                self._available.append(resource)

    def available_count(self) -> int:
        """Return number of available resources."""
        with self._lock:
            return len(self._available)

    def in_use_count(self) -> int:
        """Return number of resources in use."""
        with self._lock:
            return len(self._in_use)
