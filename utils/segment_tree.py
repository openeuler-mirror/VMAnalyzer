#!/usr/bin/env python3
"""Segment tree for range sum queries."""
from typing import List, Optional

class SegmentTree:
    def __init__(self, data: List[int]):
        self._n = len(data)
        self._tree = [0] * (4 * self._n)
        if data:
            self._build(data, 0, 0, self._n - 1)

    def _build(self, data: List[int], node: int, start: int, end: int) -> None:
        if start == end:
            self._tree[node] = data[start]
        else:
            mid = (start + end) // 2
            self._build(data, 2*node+1, start, mid)
            self._build(data, 2*node+2, mid+1, end)
            self._tree[node] = self._tree[2*node+1] + self._tree[2*node+2]

    def update(self, idx: int, val: int) -> None:
        self._update(0, 0, self._n - 1, idx, val)

    def _update(self, node: int, start: int, end: int, idx: int, val: int) -> None:
        if start == end:
            self._tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self._update(2*node+1, start, mid, idx, val)
            else:
                self._update(2*node+2, mid+1, end, idx, val)
            self._tree[node] = self._tree[2*node+1] + self._tree[2*node+2]

    def query(self, left: int, right: int) -> int:
        return self._query(0, 0, self._n - 1, left, right)

    def _query(self, node, start, end, left, right):
        if right < start or left > end:
            return 0
        if left <= start and end <= right:
            return self._tree[node]
        mid = (start + end) // 2
        return self._query(2*node+1, start, mid, left, right) + \
               self._query(2*node+2, mid+1, end, left, right)
