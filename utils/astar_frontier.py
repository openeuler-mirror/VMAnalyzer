"""A* search frontier tracking the best known cost per node.

The frontier is a min-heap keyed by estimated total cost.  Entries that were
superseded by a cheaper push are discarded lazily on pop, so callers can push
freely without maintaining an explicit decrease-key operation.
"""

import heapq
import logging
from typing import Dict, List, Optional, Tuple

LOG = logging.getLogger(__name__)


class AStarFrontier:
    """Priority frontier that skips stale entries using best g-scores."""

    def __init__(self) -> None:
        self._heap: List[Tuple[float, float, object]] = []
        self._best: Dict[object, float] = {}

    def push(self, node: object, cost_so_far: float, heuristic: float) -> None:
        """Offer *node* with total estimated cost ``cost + heuristic``."""
        if node in self._best and self._best[node] <= cost_so_far:
            return
        self._best[node] = cost_so_far
        heapq.heappush(self._heap, (cost_so_far + heuristic, cost_so_far, node))

    def pop(self) -> Optional[Tuple[object, float]]:
        """Return the cheapest live node and its cost, or None when empty."""
        while self._heap:
            _, cost_so_far, node = heapq.heappop(self._heap)
            if self._best.get(node) == cost_so_far:
                del self._best[node]
                return node, cost_so_far
        return None

    def known_cost(self, node: object) -> Optional[float]:
        """Return the best recorded cost for *node* if still pending."""
        return self._best.get(node)

    def __len__(self) -> int:
        return len(self._best)


__all__ = ["AStarFrontier"]
