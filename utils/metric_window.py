#!/usr/bin/env python3
"""Time-windowed metric collection for sliding window analysis."""
import time
from collections import deque
from typing import Deque, List, Tuple

class MetricWindow:
    """Collects metrics within a sliding time window."""

    def __init__(self, window_seconds: float = 60.0):
        self._window = window_seconds
        self._data: Deque[Tuple[float, float]] = deque()

    def add(self, value: float, timestamp: float = None) -> None:
        """Add a metric sample."""
        ts = timestamp if timestamp else time.time()
        self._data.append((ts, value))
        self._purge(ts)

    def _purge(self, now: float) -> None:
        """Remove expired entries."""
        cutoff = now - self._window
        while self._data and self._data[0][0] < cutoff:
            self._data.popleft()

    def values(self) -> List[float]:
        """Return all values in current window."""
        now = time.time()
        self._purge(now)
        return [v for _, v in self._data]

    def average(self) -> float:
        """Calculate average of values in window."""
        vals = self.values()
        return sum(vals) / len(vals) if vals else 0.0

    def count(self) -> int:
        """Return number of samples in window."""
        return len(self.values())
