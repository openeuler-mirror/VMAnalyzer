"""Suppress alerts that re-fire within a hold-down period.

A flapping VM can emit dozens of identical pages per hour.  Hold-down keeps
the first notification and drops repeats until the quiet period elapses,
while exposing the suppressed count for review.
"""

import logging
import time
from typing import Dict, Optional

LOG = logging.getLogger(__name__)


class HoldDownGate:
    """Track last notification time per alert fingerprint."""

    def __init__(self, period: float = 300.0, clock=None):
        if period < 0:
            raise ValueError("period must not be negative")
        self.period = period
        self.clock = clock or time.time
        self._last: Dict[str, float] = {}
        self.suppressed = 0

    def should_notify(self, fingerprint: str) -> bool:
        """Return True when the fingerprint has been quiet long enough."""
        now = self.clock()
        previous = self._last.get(fingerprint)
        if previous is not None and now - previous < self.period:
            self.suppressed += 1
            LOG.debug("holding down alert %s for %.1fs", fingerprint, self.period)
            return False
        self._last[fingerprint] = now
        return True

    def release(self, fingerprint: str) -> None:
        """Clear hold-down state for one fingerprint."""
        self._last.pop(fingerprint, None)

    def next_allowed(self, fingerprint: str) -> Optional[float]:
        """Return the earliest time the fingerprint may notify again."""
        previous = self._last.get(fingerprint)
        return None if previous is None else previous + self.period


__all__ = ["HoldDownGate"]
