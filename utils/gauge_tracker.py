#!/usr/bin/env python3
"""Gauge metric tracking with historical values."""
import time
from collections import deque
from typing import Deque, Optional

class GaugeTracker:
    """Tracks gauge values with optional history."""

    def __init__(self, history_size: int = 100):
        self._values: Dict[str, float] = {}
        self._history: Dict[str, Deque] = {}
        self._history_size = history_size

    def set(self, name: str, value: float) -> None:
        """Set gauge value."""
        self._values[name] = value
        if name not in self._history:
            self._history[name] = deque(maxlen=self._history_size)
        self._history[name].append((time.time(), value))

    def get(self, name: str) -> Optional[float]:
        """Get current gauge value."""
        return self._values.get(name)

    def history(self, name: str) -> list:
        """Return historical values for a gauge."""
        return list(self._history.get(name, []))

    def delta(self, name: str) -> Optional[float]:
        """Return change since last set."""
        hist = self._history.get(name, [])
        if len(hist) < 2:
            return None
        return hist[-1][1] - hist[-2][1]

    def names(self) -> list:
        """Return all gauge names."""
        return list(self._values.keys())
