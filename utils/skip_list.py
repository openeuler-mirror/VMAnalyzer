#!/usr/bin/env python3
"""Skip list for ordered key-value storage."""
import random
from typing import Any, Optional

class SkipNode:
    def __init__(self, key: int, val: Any, level: int):
        self.key = key
        self.val = val
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level: int = 16, p: float = 0.5):
        self._max_level = max_level
        self._p = p
        self._level = 0
        self._head = SkipNode(0, None, max_level)

    def _random_level(self) -> int:
        lvl = 0
        while random.random() < self._p and lvl < self._max_level:
            lvl += 1
        return lvl

    def insert(self, key: int, val: Any) -> None:
        update = [self._head] * (self._max_level + 1)
        curr = self._head
        for i in range(self._level, -1, -1):
            while curr.forward[i] and curr.forward[i].key < key:
                curr = curr.forward[i]
            update[i] = curr
        lvl = self._random_level()
        if lvl > self._level:
            self._level = lvl
        node = SkipNode(key, val, lvl)
        for i in range(lvl + 1):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node

    def search(self, key: int) -> Optional[Any]:
        curr = self._head
        for i in range(self._level, -1, -1):
            while curr.forward[i] and curr.forward[i].key < key:
                curr = curr.forward[i]
        curr = curr.forward[0]
        return curr.val if curr and curr.key == key else None
