#!/usr/bin/env python3
"""Interval tree for efficient time range queries."""
from typing import List, Tuple

class IntervalNode:
    """A node in the interval tree."""
    def __init__(self, interval: Tuple[float, float], value=None):
        self.interval = interval
        self.value = value
        self.max_end = interval[1]
        self.left = None
        self.right = None

class IntervalTree:
    """Binary search tree for interval overlap queries."""

    def __init__(self):
        self._root = None

    def insert(self, start: float, end: float, value=None) -> None:
        """Insert an interval."""
        self._root = self._insert(self._root, (start, end), value)

    def _insert(self, node, interval, value):
        if node is None:
            return IntervalNode(interval, value)
        if interval[0] < node.interval[0]:
            node.left = self._insert(node.left, interval, value)
        else:
            node.right = self._insert(node.right, interval, value)
        if interval[1] > node.max_end:
            node.max_end = interval[1]
        return node

    def find_overlaps(self, start: float, end: float) -> List:
        """Find all intervals overlapping [start, end]."""
        results = []
        self._find(self._root, start, end, results)
        return results

    def _find(self, node, start, end, results):
        if node is None:
            return
        if node.interval[0] <= end and node.interval[1] >= start:
            results.append((node.interval, node.value))
        if node.left and node.left.max_end >= start:
            self._find(node.left, start, end, results)
        self._find(node.right, start, end, results)
