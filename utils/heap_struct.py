#!/usr/bin/env python3
"""Min-heap implementation with priority queue."""
from typing import List, Any, Optional

class MinHeap:
    def __init__(self):
        self._heap: List[Any] = []

    def push(self, val: Any) -> None:
        self._heap.append(val)
        self._sift_up(len(self._heap) - 1)

    def pop(self) -> Optional[Any]:
        if not self._heap:
            return None
        if len(self._heap) == 1:
            return self._heap.pop()
        top = self._heap[0]
        self._heap[0] = self._heap.pop()
        self._sift_down(0)
        return top

    def peek(self) -> Optional[Any]:
        return self._heap[0] if self._heap else None

    def size(self) -> int:
        return len(self._heap)

    def _sift_up(self, idx: int) -> None:
        while idx > 0:
            parent = (idx - 1) // 2
            if self._heap[idx] < self._heap[parent]:
                self._heap[idx], self._heap[parent] = self._heap[parent], self._heap[idx]
                idx = parent
            else:
                break

    def _sift_down(self, idx: int) -> None:
        n = len(self._heap)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2
            if left < n and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < n and self._heap[right] < self._heap[smallest]:
                smallest = right
            if smallest != idx:
                self._heap[idx], self._heap[smallest] = self._heap[smallest], self._heap[idx]
                idx = smallest
            else:
                break
