"""K-core decomposition producing a core number for every node.

Repeatedly removing the current minimum-degree vertex yields the core number
of each node, equal to its degree at the moment it is stripped.  A heap keeps
the removal order efficient even though degrees change as neighbours leave.
"""

import heapq
import logging
from collections import defaultdict
from typing import Dict, Iterable, List, Set, Tuple

LOG = logging.getLogger(__name__)


def core_numbers(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> Dict[str, int]:
    """Compute the core number of every node in an undirected graph."""
    adjacency: Dict[str, Set[str]] = defaultdict(set)
    for left, right in edges:
        if left != right:
            adjacency[left].add(right)
            adjacency[right].add(left)
    for node in nodes:
        adjacency.setdefault(node, set())
    degree = {node: len(neighbours) for node, neighbours in adjacency.items()}
    heap = [(value, node) for node, value in degree.items()]
    heapq.heapify(heap)
    removed: Set[str] = set()
    core: Dict[str, int] = {}
    while heap:
        value, node = heapq.heappop(heap)
        if node in removed or value != degree[node]:
            continue
        removed.add(node)
        core[node] = value
        for neighbour in adjacency[node]:
            if neighbour not in removed:
                degree[neighbour] -= 1
                heapq.heappush(heap, (degree[neighbour], neighbour))
    LOG.debug("computed core numbers for %d nodes", len(core))
    return core


def max_core(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> int:
    """Return the maximum core number of the graph."""
    core = core_numbers(nodes, edges)
    return max(core.values()) if core else 0


def nodes_in_core(nodes, edges, threshold: int) -> List[str]:
    """Return nodes whose core number is at least *threshold*."""
    core = core_numbers(nodes, edges)
    return sorted(node for node, value in core.items() if value >= threshold)


__all__ = ["core_numbers", "max_core", "nodes_in_core"]
