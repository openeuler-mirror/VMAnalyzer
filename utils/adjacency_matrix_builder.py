"""Adjacency matrix construction from weighted edge lists.

Given a stable node ordering, each edge is written into a dense square matrix
at the positions of its endpoints.  Undirected edges are mirrored so the
matrix stays symmetric, which suits small dense graphs and algebra routines.
"""

import logging
from typing import Dict, Iterable, List, Sequence, Tuple

LOG = logging.getLogger(__name__)


def build_adjacency_matrix(nodes: Sequence[str], edges: Iterable[Tuple[str, str, float]],
                           directed: bool = False) -> List[List[float]]:
    """Return a dense weight matrix with edges placed at their endpoints."""
    index: Dict[str, int] = {node: position for position, node in enumerate(nodes)}
    size = len(nodes)
    matrix = [[0.0] * size for _ in range(size)]
    placed = 0
    for source, target, weight in edges:
        if source not in index or target not in index:
            continue
        matrix[index[source]][index[target]] = weight
        placed += 1
        if not directed:
            matrix[index[target]][index[source]] = weight
    LOG.debug("placed %d edges into a %dx%d matrix", placed, size, size)
    return matrix


def neighbours_of(matrix: Sequence[Sequence[float]], row: int) -> List[int]:
    """List column indices joined to *row* by a non-zero weight."""
    return [column for column, weight in enumerate(matrix[row]) if weight]


def node_index(nodes: Sequence[str]) -> Dict[str, int]:
    """Stable lookup from node label to its matrix row."""
    return {node: position for position, node in enumerate(nodes)}


__all__ = ["build_adjacency_matrix", "neighbours_of", "node_index"]
