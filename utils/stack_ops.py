#!/usr/bin/env python3
"""Stack with minimum and maximum tracking."""
from typing import Any, Optional

class MinMaxStack:
    def __init__(self):
        self._stack = []
        self._min_stack = []
        self._max_stack = []

    def push(self, val: Any) -> None:
        self._stack.append(val)
        if not self._min_stack or val <= self._min_stack[-1]:
            self._min_stack.append(val)
        if not self._max_stack or val >= self._max_stack[-1]:
            self._max_stack.append(val)

    def pop(self) -> Optional[Any]:
        if not self._stack:
            return None
        val = self._stack.pop()
        if val == self._min_stack[-1]:
            self._min_stack.pop()
        if val == self._max_stack[-1]:
            self._max_stack.pop()
        return val

    def top(self) -> Optional[Any]:
        return self._stack[-1] if self._stack else None

    def get_min(self) -> Optional[Any]:
        return self._min_stack[-1] if self._min_stack else None

    def get_max(self) -> Optional[Any]:
        return self._max_stack[-1] if self._max_stack else None

    def is_empty(self) -> bool:
        return len(self._stack) == 0

    def size(self) -> int:
        return len(self._stack)
