"""Stack with a hard capacity limit that discards oldest entries.

Diagnostic traces collected during an incident must not grow without
bound.  Dropping the oldest frames keeps the most recent context, which is
usually the part that explains a failure.
"""

import logging
from collections import deque
from typing import Iterable, List, Optional

LOG = logging.getLogger(__name__)


class BoundedStack:
    """LIFO container that evicts the oldest element past capacity."""

    def __init__(self, capacity: int = 128):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._items = deque(maxlen=capacity)
        self.dropped = 0

    def push(self, item) -> Optional[object]:
        """Push an item, returning the evicted element when full."""
        evicted = None
        if len(self._items) == self.capacity:
            evicted = self._items[0]
            self.dropped += 1
            LOG.debug("stack full, evicting oldest entry")
        self._items.append(item)
        return evicted

    def pop(self):
        """Pop the most recently pushed item."""
        return self._items.pop() if self._items else None

    def peek(self):
        """Return the most recent item without removing it."""
        return self._items[-1] if self._items else None

    def snapshot(self) -> List:
        """Return items from oldest to newest."""
        return list(self._items)

    def extend(self, items: Iterable) -> None:
        """Push several items in order."""
        for item in items:
            self.push(item)


__all__ = ["BoundedStack"]
