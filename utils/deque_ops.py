#!/usr/bin/env python3
"""Double-ended queue with rotation and slicing."""
from typing import Any, Optional, List

class Deque:
    def __init__(self):
        self._data = []

    def push_front(self, val: Any) -> None:
        self._data.insert(0, val)

    def push_back(self, val: Any) -> None:
        self._data.append(val)

    def pop_front(self) -> Optional[Any]:
        return self._data.pop(0) if self._data else None

    def pop_back(self) -> Optional[Any]:
        return self._data.pop() if self._data else None

    def rotate(self, k: int) -> None:
        if not self._data:
            return
        k = k % len(self._data)
        if k > 0:
            self._data = self._data[-k:] + self._data[:-k]
        elif k < 0:
            self._data = self._data[-k:] + self._data[:-k]

    def slice(self, start: int, end: int) -> List[Any]:
        return self._data[start:end]

    def reverse(self) -> None:
        self._data.reverse()

    def size(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def to_list(self) -> List[Any]:
        return self._data[:]
