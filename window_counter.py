"""Sliding window counter for tracking events within a time bound."""

import time
from typing import Optional
from collections import deque


class SlidingWindowCounter:
    """Counts events within a sliding time window."""

    def __init__(self, window_seconds: float) -> None:
        if window_seconds <= 0:
            raise ValueError("window_seconds must be positive")
        self._window = window_seconds
        self._events: deque = deque()

    def add(self, count: float = 1) -> None:
        now = time.monotonic()
        self._events.append((now, count))
        self._purge(now)

    def _purge(self, now: float) -> None:
        cutoff = now - self._window
        while self._events and self._events[0][0] < cutoff:
            self._events.popleft()

    def total(self) -> float:
        now = time.monotonic()
        self._purge(now)
        return sum(c for _, c in self._events)

    def count(self) -> int:
        now = time.monotonic()
        self._purge(now)
        return len(self._events)

    def rate(self) -> float:
        total = self.total()
        return total / self._window if self._window > 0 else 0.0

    def peek_oldest(self) -> Optional[float]:
        if self._events:
            return self._events[0][0]
        return None

    @property
    def window_seconds(self) -> float:
        return self._window

    def clear(self) -> None:
        self._events.clear()
