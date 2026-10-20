"""Bridge detection using DFS discovery and low-link values.

An undirected edge is a bridge when the low value of the deeper endpoint
exceeds the discovery time of the shallower one, meaning no back edge escapes
the subtree it leads into.  Parallel edges are handled by tracking edge ids.
"""

import logging
from collections import defaultdict
from typing import Dict, Iterable, List, Set, Tuple

LOG = logging.getLogger(__name__)


def find_bridges(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> Set[Tuple[str, str]]:
    """Return undirected edges whose removal disconnects the graph."""
    edge_list = list(edges)
    graph: Dict[str, List[Tuple[str, int]]] = defaultdict(list)
    for edge_id, (left, right) in enumerate(edge_list):
        graph[left].append((right, edge_id))
        graph[right].append((left, edge_id))
    for node in nodes:
        graph.setdefault(node, [])
    discovery: Dict[str, int] = {}
    low: Dict[str, int] = {}
    bridges: Set[Tuple[str, str]] = set()
    clock = [0]

    def dfs(node: str, parent_edge: int) -> None:
        discovery[node] = low[node] = clock[0]
        clock[0] += 1
        for neighbour, edge_id in graph[node]:
            if edge_id == parent_edge:
                continue
            if neighbour in discovery:
                low[node] = min(low[node], discovery[neighbour])
            else:
                dfs(neighbour, edge_id)
                low[node] = min(low[node], low[neighbour])
                if low[neighbour] > discovery[node]:
                    left, right = edge_list[edge_id]
                    bridges.add((left, right) if left <= right else (right, left))

    for node in graph:
        if node not in discovery:
            dfs(node, -1)
    LOG.debug("detected %d bridges", len(bridges))
    return bridges


def has_bridge(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> bool:
    """Return True when the graph contains at least one bridge."""
    return bool(find_bridges(nodes, edges))


__all__ = ["find_bridges", "has_bridge"]
