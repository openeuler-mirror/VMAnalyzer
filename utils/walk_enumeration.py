"""Enumeration and counting of bounded-length walks in a directed graph.

A walk may revisit nodes and edges, unlike a simple path.  Walks up to a
requested length are enumerated depth-first with a cap on results, while the
count is computed by dynamic programming over step counts.
"""

import logging
from collections import defaultdict
from typing import Dict, Iterable, List, Tuple

LOG = logging.getLogger(__name__)

Edge = Tuple[str, str]


def _adjacency(edges: Iterable[Edge]) -> Dict[str, List[str]]:
    graph: Dict[str, List[str]] = defaultdict(list)
    for source, target in edges:
        graph[source].append(target)
    return graph


def enumerate_walks(edges: Iterable[Edge], start: str, length: int, limit: int = 10000) -> List[List[str]]:
    """List walks of exactly *length* edges beginning at *start*."""
    graph = _adjacency(edges)
    results: List[List[str]] = []
    stack = [[start]]
    while stack and len(results) < limit:
        path = stack.pop()
        if len(path) - 1 == length:
            results.append(path)
            continue
        for target in graph[path[-1]]:
            stack.append(path + [target])
    LOG.debug("enumerated %d walks of length %d", len(results), length)
    return results


def count_walks(edges: Iterable[Edge], start: str, length: int) -> int:
    """Count walks of the given length without storing each path."""
    graph = _adjacency(edges)
    frontier: Dict[str, int] = {start: 1}
    for _ in range(length):
        following: Dict[str, int] = defaultdict(int)
        for node, ways in frontier.items():
            for target in graph[node]:
                following[target] += ways
        frontier = dict(following)
    return sum(frontier.values())


__all__ = ["enumerate_walks", "count_walks"]
