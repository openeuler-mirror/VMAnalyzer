#!/usr/bin/env python3
"""Priority queue with custom comparator support."""
import heapq
from typing import Any, Callable, List, Optional

class PriorityQueue:
    def __init__(self, comparator: Callable = None):
        self._heap: List = []
        self._comparator = comparator or (lambda a, b: a < b)
        self._counter = 0

    def push(self, item: Any) -> None:
        priority = self._comparator(item, item)
        heapq.heappush(self._heap, (self._counter, item))
        self._counter += 1

    def push_with_priority(self, priority: int, item: Any) -> None:
        heapq.heappush(self._heap, (priority, self._counter, item))
        self._counter += 1

    def pop(self) -> Optional[Any]:
        if not self._heap:
            return None
        return heapq.heappop(self._heap)[-1]

    def peek(self) -> Optional[Any]:
        return self._heap[0][-1] if self._heap else None

    def size(self) -> int:
        return len(self._heap)

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def clear(self) -> None:
        self._heap.clear()
        self._counter = 0
