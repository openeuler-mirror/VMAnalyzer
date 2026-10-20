"""Diagonal traversal of a matrix in zig-zag order.

Anti-diagonals are indexed by the sum of their row and column coordinates.
Each diagonal is emitted in one direction and the direction flips between
consecutive diagonals, mirroring the classic zig-zag read of a grid.
"""

import logging
from typing import List, Sequence

LOG = logging.getLogger(__name__)


def diagonal_order(matrix: Sequence[Sequence]) -> List:
    """Return elements ordered by anti-diagonals with alternating direction."""
    result: List = []
    rows = len(matrix)
    if not rows:
        return result
    columns = len(matrix[0])
    for diagonal in range(rows + columns - 1):
        top = max(0, diagonal - columns + 1)
        bottom = min(rows - 1, diagonal)
        group = [matrix[row][diagonal - row] for row in range(top, bottom + 1)]
        if diagonal % 2 == 0:
            group.reverse()
        result.extend(group)
    LOG.debug("diagonal traversal produced %d values", len(result))
    return result


def diagonal_sums(matrix: Sequence[Sequence]) -> List[int]:
    """Return the summed value of every anti-diagonal."""
    rows = len(matrix)
    columns = len(matrix[0]) if rows else 0
    sums: List[int] = []
    for diagonal in range(rows + columns - 1):
        top = max(0, diagonal - columns + 1)
        bottom = min(rows - 1, diagonal)
        sums.append(sum(matrix[row][diagonal - row] for row in range(top, bottom + 1)))
    return sums


__all__ = ["diagonal_order", "diagonal_sums"]
