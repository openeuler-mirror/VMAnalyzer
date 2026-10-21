"""Recommend NUMA nodes that best satisfy a hugepage request.

Allocating hugepages on a remote node doubles memory latency for the guest.
Ranking nodes by free hugepages and distance gives a deterministic
recommendation that the enablement tooling can apply.
"""

import logging
from typing import Dict, List, Tuple

LOG = logging.getLogger(__name__)

Distance = Dict[Tuple[int, int], int]


def default_distance(nodes: int) -> Distance:
    """Return a 10/20 style distance table for the given node count."""
    distances: Distance = {}
    for source in range(nodes):
        for target in range(nodes):
            distances[(source, target)] = 10 if source == target else 20
    return distances


def rank_nodes(requested: int, free: Dict[int, int], local_node: int,
               distances: Distance = None) -> List[Tuple[int, int, int]]:
    """Return ``(node, distance, available)`` ordered by suitability."""
    table = distances if distances is not None else default_distance(64)
    candidates = []
    for node, available in free.items():
        if available < requested:
            continue
        distance = table.get((local_node, node), 20)
        candidates.append((node, distance, int(available)))
    candidates.sort(key=lambda item: (item[1], -item[2], item[0]))
    if not candidates:
        LOG.warning("no NUMA node can satisfy a request of %d hugepage(s)", requested)
    return candidates


def best_node(requested: int, free: Dict[int, int], local_node: int) -> int:
    """Return the recommended node, or -1 when none qualifies."""
    ranked = rank_nodes(requested, free, local_node)
    return ranked[0][0] if ranked else -1


__all__ = ["Distance", "default_distance", "rank_nodes", "best_node"]
