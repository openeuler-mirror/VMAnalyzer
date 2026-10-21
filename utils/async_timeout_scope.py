"""Enforce a deadline across a group of asynchronous operations.

Collectors must abandon a slow VM probe without leaving orphan tasks.
Tracking the deadline once per round avoids re-deriving remaining time in
every nested call.
"""

import logging
import time
from typing import Optional

LOG = logging.getLogger(__name__)


class TimeoutScope:
    """Track a deadline and expose remaining time to nested operations."""

    def __init__(self, seconds: float, clock=None) -> None:
        if seconds <= 0:
            raise ValueError("seconds must be positive")
        self.clock = clock or time.monotonic
        self.deadline = self.clock() + seconds
        self.total = seconds

    def remaining(self) -> float:
        """Return the seconds left before the deadline."""
        return max(0.0, self.deadline - self.clock())

    def expired(self) -> bool:
        """Return True when the deadline has passed."""
        return self.remaining() <= 0.0

    def clamp(self, requested: Optional[float]) -> float:
        """Cap a per-operation timeout to what remains in the scope."""
        left = self.remaining()
        if requested is None:
            return left
        return max(0.0, min(float(requested), left))

    def check(self, operation: str = "operation") -> None:
        """Raise TimeoutError when the scope has expired."""
        if self.expired():
            LOG.warning("%s exceeded the %.1fs scope", operation, self.total)
            raise TimeoutError("{} timed out after {:.1f}s".format(operation, self.total))


__all__ = ["TimeoutScope"]
