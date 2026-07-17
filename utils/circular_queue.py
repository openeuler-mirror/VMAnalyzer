#!/usr/bin/env python3
"""Circular queue implementation for fixed-size buffering."""
from typing import Any, List, Optional

class CircularQueue:
    """A fixed-size circular queue with O(1) enqueue/dequeue."""

    def __init__(self, capacity: int = 100):
        self._capacity = capacity
        self._data: List[Any] = [None] * capacity
        self._head = 0
        self._tail = 0
        self._size = 0

    def enqueue(self, item: Any) -> bool:
        """Add item to queue. Returns False if full."""
        if self._size == self._capacity:
            return False
        self._data[self._tail] = item
        self._tail = (self._tail + 1) % self._capacity
        self._size += 1
        return True

    def dequeue(self) -> Optional[Any]:
        """Remove and return front item."""
        if self._size == 0:
            return None
        item = self._data[self._head]
        self._data[self._head] = None
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        return item

    def peek(self) -> Optional[Any]:
        """View front item without removing."""
        if self._size == 0:
            return None
        return self._data[self._head]

    def is_full(self) -> bool:
        return self._size == self._capacity

    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size
