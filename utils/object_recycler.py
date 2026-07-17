#!/usr/bin/env python3
"""Object recycling to reduce garbage collection pressure."""
from typing import Any, Callable, Dict, List

class ObjectRecycler:
    """Recycles objects by type to minimize allocations."""

    def __init__(self):
        self._bins: Dict[str, List[Any]] = {}
        self._resetters: Dict[str, Callable] = {}

    def register(self, type_name: str, factory: Callable, resetter: Callable) -> None:
        """Register a recyclable type with factory and reset function."""
        self._bins[type_name] = []
        self._resetters[type_name] = resetter

    def obtain(self, type_name: str) -> Any:
        """Get a recycled object or create new one."""
        if type_name in self._bins and self._bins[type_name]:
            return self._bins[type_name].pop()
        raise KeyError(f"Type '{type_name}' not registered")

    def recycle(self, type_name: str, obj: Any) -> None:
        """Return an object for recycling."""
        if type_name in self._resetters:
            self._resetters[type_name](obj)
            self._bins[type_name].append(obj)

    def stats(self) -> Dict[str, int]:
        """Return recycling statistics."""
        return {k: len(v) for k, v in self._bins.items()}
