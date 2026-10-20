"""Stoer-Wagner minimum cut value for an undirected weighted graph.

The algorithm repeatedly performs a maximum adjacency search to merge the two
most tightly connected supernodes, recording the cut of the strongly ordered
phase.  The smallest cut seen across all phases is the global minimum cut.
"""

import logging
from typing import Iterable, List, Sequence, Tuple

LOG = logging.getLogger(__name__)

WeightedEdge = Tuple[int, int, float]


def stoer_wagner(size: int, edges: Iterable[WeightedEdge]) -> float:
    """Return the value of the global minimum cut of the graph."""
    weights = [[0.0] * size for _ in range(size)]
    for left, right, weight in edges:
        weights[left][right] += weight
        weights[right][left] += weight
    vertices = list(range(size))
    best = float("inf")
    while len(vertices) > 1:
        count = len(vertices)
        used = [False] * count
        connected = [0.0] * count
        previous = -1
        for phase in range(count):
            selected = -1
            for index in range(count):
                if not used[index] and (selected < 0 or connected[index] > connected[selected]):
                    selected = index
            used[selected] = True
            if phase == count - 1:
                best = min(best, connected[selected])
                for index in range(count):
                    if not used[index]:
                        weights[vertices[previous]][vertices[index]] += weights[vertices[selected]][vertices[index]]
                        weights[vertices[index]][vertices[previous]] = weights[vertices[previous]][vertices[index]]
                vertices.pop(selected)
                break
            previous = selected
            for index in range(count):
                if not used[index]:
                    connected[index] += weights[vertices[selected]][vertices[index]]
    LOG.debug("minimum cut value %.4f", best)
    return best


def min_cut_value(size: int, edges: Iterable[WeightedEdge]) -> float:
    """Convenience wrapper returning only the minimum cut value."""
    return stoer_wagner(size, edges)


def edge_weight_sum(edges: Sequence[WeightedEdge]) -> float:
    """Return the total weight of all supplied edges."""
    return sum(weight for _, _, weight in edges)


__all__ = ["stoer_wagner", "min_cut_value", "edge_weight_sum"]
