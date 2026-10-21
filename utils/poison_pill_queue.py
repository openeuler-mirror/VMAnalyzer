"""Thread-safe queue that shuts workers down without dropping work.

Sentinel based shutdown is easy to get wrong when several workers read the
same queue.  This wrapper re-queues the sentinel after each consumer so
every worker observes the shutdown signal exactly once.
"""

import logging
import queue
from typing import Optional

LOG = logging.getLogger(__name__)


class PoisonPillQueue:
    """Bounded queue that broadcasts a shutdown sentinel to all workers."""

    def __init__(self, maxsize: int = 0) -> None:
        self._queue: "queue.Queue" = queue.Queue(maxsize=maxsize)
        self._sentinel = object()
        self._consumers = 0

    def register_consumer(self) -> None:
        """Declare one more worker that will consume the sentinel."""
        self._consumers += 1

    def put(self, item) -> None:
        """Enqueue a work item."""
        self._queue.put(item)

    def get(self, timeout: Optional[float] = None):
        """Return the next item, re-broadcasting the sentinel when seen."""
        item = self._queue.get(timeout=timeout) if timeout else self._queue.get()
        if item is self._sentinel:
            self._consumers -= 1
            if self._consumers > 0:
                self._queue.put(self._sentinel)
            LOG.debug("worker received shutdown sentinel, %d consumer(s) left",
                      self._consumers)
            return None
        return item

    def close(self) -> None:
        """Broadcast the shutdown sentinel to every registered consumer."""
        self._queue.put(self._sentinel)

    def depth(self) -> int:
        """Return the current queue depth."""
        return self._queue.qsize()


__all__ = ["PoisonPillQueue"]
