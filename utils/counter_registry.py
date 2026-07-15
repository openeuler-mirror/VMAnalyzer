#!/usr/bin/env python3
"""Named counter registry for tracking metric values."""
from typing import Dict, List

class CounterRegistry:
    """Registry of named counters with tag support."""

    def __init__(self):
        self._counters: Dict[str, float] = {}
        self._tags: Dict[str, List[str]] = {}

    def register(self, name: str, tags: List[str] = None) -> None:
        """Register a new counter."""
        if name not in self._counters:
            self._counters[name] = 0.0
            self._tags[name] = tags or []

    def increment(self, name: str, value: float = 1.0) -> None:
        """Increment a counter."""
        if name not in self._counters:
            self.register(name)
        self._counters[name] += value

    def get(self, name: str) -> float:
        """Get counter value."""
        return self._counters.get(name, 0.0)

    def reset(self, name: str) -> None:
        """Reset a counter to zero."""
        if name in self._counters:
            self._counters[name] = 0.0

    def all_counters(self) -> Dict[str, float]:
        """Return all counter values."""
        return dict(self._counters)

    def find_by_tag(self, tag: str) -> Dict[str, float]:
        """Find counters by tag."""
        return {n: v for n, v in self._counters.items() if tag in self._tags.get(n, [])}
