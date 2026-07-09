#!/usr/bin/env python3
"""Circular ring buffer for fixed-size data streaming."""
from typing import Any, Optional, List

class RingBuffer:
    def __init__(self, capacity: int):
        self._capacity = capacity
        self._buffer = [None] * capacity
        self._head = 0
        self._count = 0

    def write(self, data: Any) -> bool:
        idx = (self._head + self._count) % self._capacity
        if self._count == self._capacity:
            self._buffer[self._head] = data
            self._head = (self._head + 1) % self._capacity
            return True
        self._buffer[idx] = data
        self._count += 1
        return True

    def read(self) -> Optional[Any]:
        if self._count == 0:
            return None
        val = self._buffer[self._head]
        self._head = (self._head + 1) % self._capacity
        self._count -= 1
        return val

    def peek(self) -> Optional[Any]:
        if self._count == 0:
            return None
        return self._buffer[self._head]

    def is_full(self) -> bool:
        return self._count == self._capacity

    def is_empty(self) -> bool:
        return self._count == 0

    def to_list(self) -> List[Any]:
        result = []
        for i in range(self._count):
            idx = (self._head + i) % self._capacity
            result.append(self._buffer[idx])
        return result
