"""One-shot countdown barrier for coordinating collector rounds.

A collection round should start only after every per-VM probe reported in.
Using a countdown barrier keeps the coordinator free of polling loops and
makes partial rounds observable.
"""

import logging
import threading
from typing import Optional

LOG = logging.getLogger(__name__)


class CountdownBarrier:
    """Release waiters once the arrival count reaches the target."""

    def __init__(self, parties: int, timeout: Optional[float] = None):
        if parties <= 0:
            raise ValueError("parties must be positive")
        self.parties = parties
        self.timeout = timeout
        self._remaining = parties
        self._condition = threading.Condition()
        self._broken = False

    def arrive(self) -> bool:
        """Record one arrival, returning True for the last participant."""
        with self._condition:
            if self._broken:
                return False
            self._remaining -= 1
            if self._remaining <= 0:
                self._condition.notify_all()
                LOG.debug("barrier released after %d arrival(s)", self.parties)
                return True
            return False

    def wait(self) -> bool:
        """Block until all parties arrive, returning False on timeout."""
        with self._condition:
            completed = self._condition.wait_for(
                lambda: self._remaining <= 0 or self._broken, timeout=self.timeout)
            if not completed:
                LOG.warning("barrier timed out with %d outstanding party(ies)", self._remaining)
            return completed

    def abort(self) -> None:
        """Break the barrier so all waiters return immediately."""
        with self._condition:
            self._broken = True
            self._condition.notify_all()

    @property
    def remaining(self) -> int:
        """Return how many participants have not arrived yet."""
        return max(0, self._remaining)


__all__ = ["CountdownBarrier"]
