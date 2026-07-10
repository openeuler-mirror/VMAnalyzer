#!/usr/bin/env python3
"""Union-find with path compression and union by rank."""
from typing import Dict, List

class UnionFind:
    def __init__(self):
        self._parent: Dict[int, int] = {}
        self._rank: Dict[int, int] = {}
        self._count = 0

    def add(self, x: int) -> None:
        if x not in self._parent:
            self._parent[x] = x
            self._rank[x] = 0
            self._count += 1

    def find(self, x: int) -> int:
        if x not in self._parent:
            self.add(x)
            return x
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self._rank[px] < self._rank[py]:
            px, py = py, px
        self._parent[py] = px
        if self._rank[px] == self._rank[py]:
            self._rank[px] += 1
        self._count -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

    def components(self) -> int:
        return self._count
