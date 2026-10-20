"""Longest weighted path in a directed acyclic graph.

Processing nodes in topological order lets every outgoing edge relax the
distance of its target exactly once.  When no source is given, each node may
serve as a starting point, which yields the global longest path value.
"""

import logging
from collections import defaultdict, deque
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

LOG = logging.getLogger(__name__)

WeightedEdge = Tuple[str, str, float]


def longest_path(nodes: Sequence[str], edges: Iterable[WeightedEdge],
                 source: Optional[str] = None) -> Dict[str, float]:
    """Return the maximum weighted distance from *source* to every node."""
    adjacency: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
    indegree: Dict[str, int] = {node: 0 for node in nodes}
    for start, end, weight in edges:
        adjacency[start].append((end, weight))
        indegree[end] = indegree.get(end, 0) + 1
    queue = deque(sorted(node for node, value in indegree.items() if value == 0))
    order: List[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for target, _ in adjacency[node]:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    distance: Dict[str, float] = {node: float("-inf") for node in order}
    if source is None:
        for node in order:
            distance[node] = 0.0
    elif source in distance:
        distance[source] = 0.0
    for node in order:
        if distance[node] == float("-inf"):
            continue
        for target, weight in adjacency[node]:
            if distance[node] + weight > distance[target]:
                distance[target] = distance[node] + weight
    LOG.debug("relaxed %d nodes in topological order", len(order))
    return distance


def critical_length(nodes: Sequence[str], edges: Iterable[WeightedEdge],
                    source: Optional[str] = None) -> float:
    """Return the longest distance recorded across all reachable nodes."""
    distance = longest_path(nodes, edges, source)
    reachable = [value for value in distance.values() if value != float("-inf")]
    return max(reachable) if reachable else 0.0


__all__ = ["longest_path", "critical_length"]
