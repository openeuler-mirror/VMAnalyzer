"""Requeue failed tasks with increasing delays instead of blocking workers.

Immediate retries amplify an outage.  A delay queue keeps failed tasks out
of the hot path while preserving their order per attempt level and keeping
the worker pool responsive.
"""

import logging
import time
from typing import Dict, List, Tuple

LOG = logging.getLogger(__name__)


class WorkerBackoffQueue:
    """Queue tasks with per-attempt delays and bounded retry counts."""

    def __init__(self, max_attempts: int = 3, base_delay: float = 1.0,
                 clock=None) -> None:
        if max_attempts <= 0:
            raise ValueError("max_attempts must be positive")
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.clock = clock or time.time
        self._pending: List[Tuple[float, int, str]] = []
        self._attempts: Dict[str, int] = {}
        self.dropped = 0

    def fail(self, name: str) -> bool:
        """Record a failure, returning True when the task was requeued."""
        attempts = self._attempts.get(name, 0) + 1
        self._attempts[name] = attempts
        if attempts >= self.max_attempts:
            self.dropped += 1
            LOG.warning("task %s dropped after %d attempt(s)", name, attempts)
            return False
        delay = self.base_delay * (2 ** (attempts - 1))
        self._pending.append((self.clock() + delay, attempts, name))
        return True

    def ready(self) -> List[str]:
        """Return tasks whose delay has elapsed."""
        now = self.clock()
        due = [item for item in self._pending if item[0] <= now]
        self._pending = [item for item in self._pending if item[0] > now]
        if due:
            LOG.debug("%d task(s) ready for retry", len(due))
        return [name for _, _, name in sorted(due)]

    def pending(self) -> int:
        """Return how many tasks are waiting for their retry time."""
        return len(self._pending)


__all__ = ["WorkerBackoffQueue"]
