"""Exponential decay counter for time-weighted metric aggregation."""

import time
from typing import Dict, Optional


class DecayCounter:
    """Applies exponential decay to counts based on elapsed time."""

    def __init__(self, half_life: float = 3600.0) -> None:
        if half_life <= 0:
            raise ValueError("half_life must be positive")
        self._half_life = half_life
        self._decay_rate = 0.6931471805599453 / half_life
        self._counts: Dict[str, float] = {}
        self._last_update: Dict[str, float] = {}

    def add(self, key: str, amount: float = 1.0) -> float:
        now = time.monotonic()
        self._apply_decay(key, now)
        self._counts[key] = self._counts.get(key, 0.0) + amount
        self._last_update[key] = now
        return self._counts[key]

    def _apply_decay(self, key: str, now: float) -> None:
        if key not in self._counts:
            return
        elapsed = now - self._last_update.get(key, now)
        if elapsed > 0:
            self._counts[key] *= 2.718281828459045 ** (-self._decay_rate * elapsed)

    def get(self, key: str) -> float:
        now = time.monotonic()
        self._apply_decay(key, now)
        self._last_update[key] = now
        return self._counts.get(key, 0.0)

    def total(self) -> float:
        now = time.monotonic()
        return sum(self._get_decayed(k, now) for k in self._counts)

    def _get_decayed(self, key: str, now: float) -> float:
        if key not in self._counts:
            return 0.0
        elapsed = now - self._last_update.get(key, now)
        return self._counts[key] * (2.718281828459045 ** (-self._decay_rate * elapsed))

    def keys(self) -> list:
        return list(self._counts.keys())

    def remove(self, key: str) -> None:
        self._counts.pop(key, None)
        self._last_update.pop(key, None)

    def clear(self) -> None:
        self._counts.clear()
        self._last_update.clear()

    @property
    def half_life(self) -> float:
        return self._half_life
