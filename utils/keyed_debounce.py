"""Debounce repeated events independently per key.

VM state changes arrive in bursts, and a global debounce would suppress
legitimate transitions on other guests.  Keying the timer by VM name keeps
the suppression local while still collapsing duplicate events.
"""

import logging
import time
from typing import Any, Callable, Dict, Optional

LOG = logging.getLogger(__name__)


class KeyedDebounce:
    """Suppress repeated calls per key within a quiet period."""

    def __init__(self, interval: float = 1.0, clock: Callable[[], float] = time.time):
        if interval < 0:
            raise ValueError("interval must not be negative")
        self.interval = interval
        self.clock = clock
        self._last: Dict[Any, float] = {}

    def ready(self, key: Any) -> bool:
        """Return True when *key* may fire, updating its last-seen time."""
        now = self.clock()
        previous = self._last.get(key)
        if previous is not None and now - previous < self.interval:
            LOG.debug("debounced key %r, %.3fs since last event", key, now - previous)
            return False
        self._last[key] = now
        return True

    def last_seen(self, key: Any) -> Optional[float]:
        """Return the timestamp of the last accepted event for *key*."""
        return self._last.get(key)

    def forget(self, key: Any) -> None:
        """Drop the debounce state for a single key."""
        self._last.pop(key, None)

    def reset(self) -> None:
        """Drop all debounce state."""
        self._last.clear()


__all__ = ["KeyedDebounce"]
