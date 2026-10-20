"""Fast exponentiation of small square integer matrices.

Repeated squaring reduces the number of multiplications to O(log exponent).
The multiply helper skips zero entries so sparse matrices cost less than the
naive triple loop suggests, which matters for adjacency-matrix powers.
"""

import logging
from typing import List, Sequence

LOG = logging.getLogger(__name__)

Matrix = List[List[int]]


def matmul(left: Sequence[Sequence[int]], right: Sequence[Sequence[int]]) -> Matrix:
    """Multiply two square matrices using a zero-skipping triple loop."""
    size = len(left)
    result = [[0] * size for _ in range(size)]
    for row in range(size):
        for pivot in range(size):
            factor = left[row][pivot]
            if factor == 0:
                continue
            for column in range(size):
                result[row][column] += factor * right[pivot][column]
    return result


def matrix_power(matrix: Sequence[Sequence[int]], exponent: int) -> Matrix:
    """Raise *matrix* to *exponent* by repeated squaring."""
    size = len(matrix)
    result = [[1 if row == column else 0 for column in range(size)] for row in range(size)]
    base = [list(row) for row in matrix]
    while exponent > 0:
        if exponent & 1:
            result = matmul(result, base)
        base = matmul(base, base)
        exponent >>= 1
    LOG.debug("matrix power computed for size %d", size)
    return result


def trace(matrix: Sequence[Sequence[int]]) -> int:
    """Return the sum of the main diagonal entries."""
    return sum(matrix[index][index] for index in range(len(matrix)))


__all__ = ["matmul", "matrix_power", "trace"]
