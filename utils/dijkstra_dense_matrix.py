"""Dijkstra shortest paths over a dense adjacency matrix.

With a dense matrix the cheapest next node can be found by scanning all
vertices, giving O(V^2) total work and avoiding a heap entirely.  This suits
graphs where nearly every pair of nodes is connected.
"""

import logging
import math
from typing import List, Sequence

LOG = logging.getLogger(__name__)

INF = math.inf


def dijkstra_matrix(matrix: Sequence[Sequence[float]], source: int) -> List[float]:
    """Return shortest distances from *source* using a linear scan."""
    size = len(matrix)
    distance = [INF] * size
    visited = [False] * size
    distance[source] = 0.0
    for _ in range(size):
        chosen = -1
        best = INF
        for node in range(size):
            if not visited[node] and distance[node] < best:
                chosen, best = node, distance[node]
        if chosen < 0:
            break
        visited[chosen] = True
        for node in range(size):
            weight = matrix[chosen][node]
            if weight > 0 and distance[chosen] + weight < distance[node]:
                distance[node] = distance[chosen] + weight
    LOG.debug("settled %d nodes from source %d", sum(visited), source)
    return distance


def unreachable_nodes(matrix: Sequence[Sequence[float]], source: int) -> List[int]:
    """Return indices that cannot be reached from *source*."""
    return [node for node, value in enumerate(dijkstra_matrix(matrix, source)) if value == INF]


def eccentricity(matrix: Sequence[Sequence[float]], source: int) -> float:
    """Return the largest finite distance from *source*."""
    finite = [value for value in dijkstra_matrix(matrix, source) if value != INF]
    return max(finite) if finite else INF


__all__ = ["dijkstra_matrix", "unreachable_nodes", "eccentricity", "INF"]
