"""Edge list deduplication and endpoint canonicalisation.

Repeated edges inflate degree counts and skew traversal work, so this module
normalises endpoints and drops duplicates while preserving first-seen order.
Undirected edges are ordered so that ``(a, b)`` and ``(b, a)`` collapse.
"""

import logging
from typing import Iterable, List, Set, Tuple

LOG = logging.getLogger(__name__)


def canonical_edge(left: str, right: str, directed: bool = False) -> Tuple[str, str]:
    """Return a normalised edge, sorting endpoints when undirected."""
    if directed or left <= right:
        return left, right
    return right, left


def dedupe_edges(edges: Iterable[Tuple[str, str]], directed: bool = False) -> List[Tuple[str, str]]:
    """Remove duplicate edges while preserving first-seen order."""
    seen: Set[Tuple[str, str]] = set()
    unique: List[Tuple[str, str]] = []
    for left, right in edges:
        key = canonical_edge(left, right, directed)
        if key in seen:
            LOG.debug("dropping duplicate edge %s", key)
            continue
        seen.add(key)
        unique.append(key)
    return unique


def count_duplicates(edges: Iterable[Tuple[str, str]], directed: bool = False) -> int:
    """Return how many supplied edges were redundant."""
    materialised = list(edges)
    return len(materialised) - len(dedupe_edges(materialised, directed))


def self_loops(edges: Iterable[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Return edges whose endpoints are identical."""
    return [(left, right) for left, right in edges if left == right]


__all__ = ["canonical_edge", "dedupe_edges", "count_duplicates", "self_loops"]
