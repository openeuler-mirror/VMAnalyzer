"""In-place matrix rotation by 90-degree increments.

A clockwise quarter turn is a transpose followed by a horizontal mirror of
each row.  Repeated application cycles through the four orientations, so any
multiple of 90 degrees can be applied with at most three passes.
"""

import logging
from typing import List, Sequence

LOG = logging.getLogger(__name__)


def rotate90(matrix: Sequence[Sequence]) -> List[List]:
    """Return a new matrix rotated 90 degrees clockwise."""
    rows = len(matrix)
    columns = len(matrix[0]) if rows else 0
    return [[matrix[rows - 1 - row][column] for row in range(rows)] for column in range(columns)]


def rotate_in_place(matrix: List[List]) -> None:
    """Rotate a square matrix 90 degrees clockwise without a copy."""
    size = len(matrix)
    for row in range(size):
        for column in range(row + 1, size):
            matrix[row][column], matrix[column][row] = matrix[column][row], matrix[row][column]
    for row in matrix:
        row.reverse()


def rotate_times(matrix: Sequence[Sequence], turns: int) -> List[List]:
    """Rotate the matrix by *turns* quarter turns clockwise."""
    result = [list(row) for row in matrix]
    for _ in range(turns % 4):
        result = rotate90(result)
    LOG.debug("rotated matrix %d quarter turns", turns % 4)
    return result


__all__ = ["rotate90", "rotate_in_place", "rotate_times"]
