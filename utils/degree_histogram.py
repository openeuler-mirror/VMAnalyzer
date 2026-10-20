"""Degree histogram statistics for undirected edge lists.

Nodes start with degree zero and each incident edge bumps their count.  The
histogram then buckets nodes by degree, which reveals hubs and leaves without
materialising the full adjacency structure.
"""

import logging
from collections import Counter
from typing import Dict, Iterable, List, Tuple

LOG = logging.getLogger(__name__)


def degree_counts(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> Dict[str, int]:
    """Return a mapping from node to its undirected degree."""
    counts: Dict[str, int] = {node: 0 for node in nodes}
    for left, right in edges:
        counts[left] = counts.get(left, 0) + 1
        counts[right] = counts.get(right, 0) + 1
    return counts


def degree_histogram(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> List[Tuple[int, int]]:
    """Return sorted ``(degree, node_count)`` pairs for the graph."""
    bucket = Counter(degree_counts(nodes, edges).values())
    histogram = sorted(bucket.items())
    LOG.debug("histogram spans %d distinct degrees", len(histogram))
    return histogram


def max_degree(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> int:
    """Return the largest degree present, or 0 for an empty graph."""
    counts = degree_counts(nodes, edges)
    return max(counts.values()) if counts else 0


def leaves(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> List[str]:
    """Return nodes with degree exactly one."""
    counts = degree_counts(nodes, edges)
    return sorted(node for node, value in counts.items() if value == 1)


__all__ = ["degree_counts", "degree_histogram", "max_degree", "leaves"]
