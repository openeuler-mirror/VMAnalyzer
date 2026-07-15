#!/usr/bin/env python3
"""Quad tree for 2D spatial data indexing."""
from typing import Any, List, Tuple

class QuadTree:
    """A quad tree for spatial range queries with automatic splitting."""

    def __init__(self, x: float, y: float, w: float, h: float, cap: int = 4):
        self._bx, self._by, self._bw, self._bh = x, y, w, h
        self._cap = cap
        self._points: List[Tuple[float, float, Any]] = []
        self._children: List["QuadTree"] = None

    def insert(self, x: float, y: float, data: Any = None) -> bool:
        if not (self._bx <= x < self._bx + self._bw and self._by <= y < self._by + self._bh):
            return False
        if self._children is None:
            if len(self._points) < self._cap:
                self._points.append((x, y, data))
                return True
            self._split()
        return any(c.insert(x, y, data) for c in self._children)

    def _split(self):
        hw, hh = self._bw / 2, self._bh / 2
        bx, by = self._bx, self._by
        self._children = [
            QuadTree(bx, by, hw, hh, self._cap),
            QuadTree(bx + hw, by, hw, hh, self._cap),
            QuadTree(bx, by + hh, hw, hh, self._cap),
            QuadTree(bx + hw, by + hh, hw, hh, self._cap),
        ]
        for x, y, d in self._points:
            for c in self._children:
                if c.insert(x, y, d):
                    break
        self._points = []

    def query_range(self, x: float, y: float, w: float, h: float) -> List:
        if self._bx >= x + w or self._bx + self._bw <= x:
            return []
        if self._by >= y + h or self._by + self._bh <= y:
            return []
        if self._children is None:
            return [p for p in self._points if x <= p[0] < x + w and y <= p[1] < y + h]
        results = []
        for c in self._children:
            results.extend(c.query_range(x, y, w, h))
        return results
