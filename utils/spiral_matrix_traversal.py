"""Clockwise spiral traversal of a matrix.

Four moving boundaries shrink toward the centre while elements are read along
the top row, right column, bottom row and left column in turn.  The guards on
the last two sweeps prevent double counting on non-square inputs.
"""

import logging
from typing import List, Sequence

LOG = logging.getLogger(__name__)


def spiral_order(matrix: Sequence[Sequence]) -> List:
    """Return the matrix elements in clockwise spiral order."""
    result: List = []
    if not matrix:
        return result
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for column in range(left, right + 1):
            result.append(matrix[top][column])
        top += 1
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1
        if top <= bottom:
            for column in range(right, left - 1, -1):
                result.append(matrix[bottom][column])
            bottom -= 1
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1
    LOG.debug("spiral emitted %d elements", len(result))
    return result


def spiral_ring_count(rows: int, columns: int) -> int:
    """Return how many concentric rings a matrix of this shape has."""
    return (min(rows, columns) + 1) // 2


__all__ = ["spiral_order", "spiral_ring_count"]
