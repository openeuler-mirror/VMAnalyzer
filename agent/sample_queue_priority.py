#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Heap based priority queue for pending samples."""

import heapq
import logging

LOG = logging.getLogger(__name__)


class SamplePriorityQueue:
    """Order pending samples by priority then arrival order."""

    def __init__(self):
        self._heap = []
        self._sequence = 0

    def push(self, item, priority=0):
        """Queue *item*; lower priority numbers are served first."""
        self._sequence += 1
        heapq.heappush(self._heap, (priority, self._sequence, item))
        return self._sequence

    def pop(self):
        """Return the next item, or None when the queue is empty."""
        if not self._heap:
            return None
        priority, _, item = heapq.heappop(self._heap)
        LOG.debug("popped item with priority %s", priority)
        return item

    def size(self):
        """Number of queued items."""
        return len(self._heap)

    def peek_priority(self):
        """Priority of the next item without removing it."""
        return self._heap[0][0] if self._heap else None
