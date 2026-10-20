"""Topological ordering that groups nodes into dependency layers.

Kahn's algorithm repeatedly peels off nodes with no remaining prerequisites.
Collecting each peeled wave separately yields the layer structure used to
visualise build graphs or to schedule independent work in parallel.
"""

import logging
from collections import defaultdict, deque
from typing import Dict, Iterable, List, Sequence, Tuple

LOG = logging.getLogger(__name__)


def topological_layers(nodes: Sequence[str], edges: Iterable[Tuple[str, str]]) -> List[List[str]]:
    """Group nodes by depth, each inner list holding one parallel wave."""
    adjacency: Dict[str, List[str]] = defaultdict(list)
    indegree: Dict[str, int] = {node: 0 for node in nodes}
    for source, target in edges:
        adjacency[source].append(target)
        indegree[target] = indegree.get(target, 0) + 1
    frontier = deque(sorted(node for node, degree in indegree.items() if degree == 0))
    layers: List[List[str]] = []
    while frontier:
        layers.append(sorted(frontier))
        following: deque = deque()
        while frontier:
            node = frontier.popleft()
            for target in adjacency[node]:
                indegree[target] -= 1
                if indegree[target] == 0:
                    following.append(target)
        frontier = following
    LOG.debug("produced %d layers", len(layers))
    return layers


def is_acyclic(nodes: Sequence[str], edges: Iterable[Tuple[str, str]]) -> bool:
    """Return True when every node appears in some topological layer."""
    total = sum(len(layer) for layer in topological_layers(nodes, edges))
    return total == len(set(nodes))


def flatten_layers(layers: List[List[str]]) -> List[str]:
    """Flatten layered output into a single valid topological order."""
    return [node for layer in layers for node in layer]


__all__ = ["topological_layers", "is_acyclic", "flatten_layers"]
