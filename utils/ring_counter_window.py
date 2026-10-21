"""Sliding-window counter backed by a fixed-size ring of buckets.

Bounded memory matters in a long running agent, so the window keeps exactly
``buckets`` slots and evicts ages rather than timestamps.  Summing the ring
gives a monotonic approximation of rates without unbounded growth.
"""

import logging
import time
from typing import List

LOG = logging.getLogger(__name__)


class RingCounterWindow:
    """Count events in a rolling window of fixed buckets."""

    def __init__(self, buckets: int = 60, slot_seconds: float = 1.0):
        if buckets <= 0 or slot_seconds <= 0:
            raise ValueError("buckets and slot_seconds must be positive")
        self.buckets = buckets
        self.slot_seconds = slot_seconds
        self._counts: List[int] = [0] * buckets
        self._slot = -1

    def _advance(self, now: float) -> None:
        """Zero out slots that fell out of the window."""
        current = int(now // self.slot_seconds)
        if self._slot < 0:
            self._slot = current
            return
        gap = current - self._slot
        if gap <= 0:
            return
        if gap >= self.buckets:
            self._counts = [0] * self.buckets
        else:
            for offset in range(gap):
                self._counts[(self._slot + offset + 1) % self.buckets] = 0
        self._slot = current

    def add(self, amount: int = 1, now: float = None) -> int:
        """Add *amount* to the current slot and return the window total."""
        reference = time.time() if now is None else now
        self._advance(reference)
        slot = self._slot % self.buckets
        self._counts[slot] += int(amount)
        return sum(self._counts)

    def total(self) -> int:
        """Return the number of events currently inside the window."""
        return sum(self._counts)

    def rate(self) -> float:
        """Return events per second across the whole window."""
        return self.total() / (self.buckets * self.slot_seconds)


__all__ = ["RingCounterWindow"]
