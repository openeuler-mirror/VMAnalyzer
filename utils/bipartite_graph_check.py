"""Bipartite test for undirected graphs via two-colouring.

A graph is bipartite exactly when it can be coloured with two colours so that
no edge joins equal colours.  A breadth-first sweep assigning the opposite
colour to each neighbour detects the first conflicting edge, if any.
"""

import logging
from collections import defaultdict, deque
from typing import Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)


def two_colour(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> Optional[Dict[str, int]]:
    """Return a 0/1 colouring of the graph, or None when not bipartite."""
    adjacency: Dict[str, List[str]] = defaultdict(list)
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    colour: Dict[str, int] = {}
    for start in nodes:
        if start in colour:
            continue
        colour[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbour in adjacency[node]:
                if neighbour not in colour:
                    colour[neighbour] = 1 - colour[node]
                    queue.append(neighbour)
                elif colour[neighbour] == colour[node]:
                    LOG.debug("conflict on edge %s-%s", node, neighbour)
                    return None
    return colour


def is_bipartite(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> bool:
    """Return True when the graph admits a valid two-colouring."""
    return two_colour(nodes, edges) is not None


def partition_sides(colouring: Optional[Dict[str, int]]) -> Tuple[List[str], List[str]]:
    """Split a valid colouring into the two sides of the partition."""
    if colouring is None:
        return [], []
    left = sorted(node for node, value in colouring.items() if value == 0)
    right = sorted(node for node, value in colouring.items() if value == 1)
    return left, right


__all__ = ["two_colour", "is_bipartite", "partition_sides"]
