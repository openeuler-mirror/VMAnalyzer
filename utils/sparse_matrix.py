#!/usr/bin/env python3
"""Sparse matrix representation for memory-efficient storage."""
from typing import Dict, List, Tuple

class SparseMatrix:
    """A sparse matrix using dictionary-of-keys representation."""

    def __init__(self, rows: int, cols: int):
        self._rows = rows
        self._cols = cols
        self._data: Dict[Tuple[int, int], float] = {}

    def set(self, row: int, col: int, value: float) -> None:
        if value != 0:
            self._data[(row, col)] = value
        elif (row, col) in self._data:
            del self._data[(row, col)]

    def get(self, row: int, col: int) -> float:
        return self._data.get((row, col), 0.0)

    def density(self) -> float:
        total = self._rows * self._cols
        return len(self._data) / total if total > 0 else 0.0

    def non_zero_count(self) -> int:
        return len(self._data)

    def multiply(self, scalar: float) -> "SparseMatrix":
        result = SparseMatrix(self._rows, self._cols)
        result._data = {k: v * scalar for k, v in self._data.items()}
        return result

    def add(self, other: "SparseMatrix") -> "SparseMatrix":
        result = SparseMatrix(self._rows, self._cols)
        result._data = dict(self._data)
        for k, v in other._data.items():
            result._data[k] = result._data.get(k, 0) + v
        result._data = {k: v for k, v in result._data.items() if v != 0}
        return result
