"""Bellman-Ford relaxation for shortest paths with negative edges.

The algorithm relaxes every edge repeatedly, so a path with at most k edges
propagates after k rounds.  A further successful relaxation after V-1 rounds
proves the reachable part of the graph contains a negative cycle.
"""

import logging
import math
from typing import List, Optional, Sequence, Tuple

LOG = logging.getLogger(__name__)

INF = math.inf
Edge = Tuple[int, int, float]


def bellman_ford(size: int, edges: Sequence[Edge], source: int) -> Tuple[List[float], bool]:
    """Return distance estimates plus a flag for a detected negative cycle."""
    distance = [INF] * size
    distance[source] = 0.0
    for round_index in range(size - 1):
        changed = False
        for start, end, weight in edges:
            if distance[start] != INF and distance[start] + weight < distance[end]:
                distance[end] = distance[start] + weight
                changed = True
        if not changed:
            LOG.debug("relaxation settled after %d rounds", round_index + 1)
            break
    negative_cycle = any(
        distance[start] != INF and distance[start] + weight < distance[end]
        for start, end, weight in edges
    )
    return distance, negative_cycle


def shortest_distance(size: int, edges: Sequence[Edge], source: int, target: int) -> Optional[float]:
    """Return the relaxed distance to *target*, or None when unreachable."""
    distance, _ = bellman_ford(size, edges, source)
    if 0 <= target < size and distance[target] != INF:
        return distance[target]
    return None


__all__ = ["bellman_ford", "shortest_distance", "Edge", "INF"]
