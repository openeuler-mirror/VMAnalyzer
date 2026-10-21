"""Order collection tasks so critical probes always run first.

When a round runs out of time, low-value probes should be dropped rather
than critical ones.  A priority heap with stable tie-breaking provides that
ordering without sorting the full task list each cycle.
"""

import heapq
import logging

LOG = logging.getLogger(__name__)

PRIORITIES = {"critical": 0, "high": 1, "normal": 2, "low": 3}


class CollectionPriorityHeap:
    """Heap of collection tasks ordered by priority then name."""

    def __init__(self):
        self._heap = []
        self._counter = 0

    def push(self, name, priority="normal"):
        """Add a task with the given priority label."""
        rank = PRIORITIES.get(str(priority).lower(), PRIORITIES["normal"])
        heapq.heappush(self._heap, (rank, self._counter, name))
        self._counter += 1

    def pop_all(self):
        """Drain the heap into an ordered list of names."""
        ordered = []
        while self._heap:
            _, _, name = heapq.heappop(self._heap)
            ordered.append(name)
        LOG.debug("drained %d task(s) in priority order", len(ordered))
        return ordered

    def pop_until(self, budget):
        """Return at most *budget* tasks, discarding the rest."""
        selected = []
        while self._heap and len(selected) < budget:
            _, _, name = heapq.heappop(self._heap)
            selected.append(name)
        if self._heap:
            LOG.info("dropped %d task(s) due to the budget of %d",
                     len(self._heap), budget)
        return selected

    def __len__(self):
        return len(self._heap)
