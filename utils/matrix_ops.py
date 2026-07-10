#!/usr/bin/env python3
"""Matrix operations including multiply and transpose."""
from typing import List

class Matrix:
    def __init__(self, data: List[List[float]]):
        self._data = data
        self._rows = len(data)
        self._cols = len(data[0]) if data else 0

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    def multiply(self, other: "Matrix") -> "Matrix":
        if self._cols != other.rows:
            raise ValueError("Incompatible dimensions")
        result = [[0] * other.cols for _ in range(self._rows)]
        for i in range(self._rows):
            for j in range(other.cols):
                for k in range(self._cols):
                    result[i][j] += self._data[i][k] * other._data[k][j]
        return Matrix(result)

    def transpose(self) -> "Matrix":
        result = [[self._data[j][i] for j in range(self._rows)] for i in range(self._cols)]
        return Matrix(result)

    def scalar_multiply(self, scalar: float) -> "Matrix":
        result = [[self._data[i][j] * scalar for j in range(self._cols)] for i in range(self._rows)]
        return Matrix(result)

    def add(self, other: "Matrix") -> "Matrix":
        result = [[self._data[i][j] + other._data[i][j] for j in range(self._cols)] for i in range(self._rows)]
        return Matrix(result)

    def to_list(self) -> List[List[float]]:
        return [row[:] for row in self._data]
