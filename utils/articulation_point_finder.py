"""Articulation point discovery via Tarjan DFS low-link values.

A vertex is an articulation point when removing it increases the number of
connected components.  The recursive DFS records discovery times and low
values; the root qualifies only with more than one DFS child.
"""

import logging
from collections import defaultdict
from typing import Dict, Iterable, List, Set, Tuple

LOG = logging.getLogger(__name__)


def articulation_points(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> Set[str]:
    """Return the set of vertices whose removal disconnects the graph."""
    graph: Dict[str, List[str]] = defaultdict(list)
    for left, right in edges:
        graph[left].append(right)
        graph[right].append(left)
    for node in nodes:
        graph.setdefault(node, [])
    discovery: Dict[str, int] = {}
    low: Dict[str, int] = {}
    points: Set[str] = set()
    clock = [0]

    def dfs(node: str, parent: str) -> None:
        discovery[node] = low[node] = clock[0]
        clock[0] += 1
        children = 0
        for neighbour in graph[node]:
            if neighbour not in discovery:
                children += 1
                dfs(neighbour, node)
                low[node] = min(low[node], low[neighbour])
                if parent is not None and low[neighbour] >= discovery[node]:
                    points.add(node)
            elif neighbour != parent:
                low[node] = min(low[node], discovery[neighbour])
        if parent is None and children > 1:
            points.add(node)

    visited: Set[str] = set()
    for node in graph:
        if node not in visited:
            dfs(node, None)
            visited.add(node)
    LOG.debug("found %d articulation points", len(points))
    return points


def is_articulation(nodes: Iterable[str], edges: Iterable[Tuple[str, str]], target: str) -> bool:
    """Return whether *target* is an articulation point."""
    return target in articulation_points(nodes, edges)


__all__ = ["articulation_points", "is_articulation"]
