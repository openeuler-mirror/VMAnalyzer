#!/usr/bin/env python3
"""Disjoint set with path halving optimization."""
from typing import Dict, List

class DisjointSet:
    def __init__(self):
        self._parent: Dict[int, int] = {}
        self._size: Dict[int, int] = {}

    def make_set(self, x: int) -> None:
        if x not in self._parent:
            self._parent[x] = x
            self._size[x] = 1

    def find(self, x: int) -> int:
        self.make_set(x)
        while self._parent[x] != x:
            self._parent[x] = self._parent[self._parent[x]]
            x = self._parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self._size[px] < self._size[py]:
            px, py = py, px
        self._parent[py] = px
        self._size[px] += self._size[py]
        return True

    def get_size(self, x: int) -> int:
        return self._size.get(self.find(x), 0)

    def count_sets(self) -> int:
        roots = set()
        for x in self._parent:
            roots.add(self.find(x))
        return len(roots)
