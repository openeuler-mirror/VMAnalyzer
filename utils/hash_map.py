#!/usr/bin/env python3
"""Hash map with separate chaining for collision resolution."""
from typing import Any, Optional, List

class HashEntry:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None

class HashMap:
    def __init__(self, capacity: int = 256):
        self._capacity = capacity
        self._buckets: List[Optional[HashEntry]] = [None] * capacity
        self._size = 0

    def _hash(self, key) -> int:
        return hash(key) % self._capacity

    def put(self, key, val) -> None:
        idx = self._hash(key)
        entry = self._buckets[idx]
        while entry:
            if entry.key == key:
                entry.val = val
                return
            entry = entry.next
        new_entry = HashEntry(key, val)
        new_entry.next = self._buckets[idx]
        self._buckets[idx] = new_entry
        self._size += 1

    def get(self, key) -> Optional[Any]:
        idx = self._hash(key)
        entry = self._buckets[idx]
        while entry:
            if entry.key == key:
                return entry.val
            entry = entry.next
        return None

    def remove(self, key) -> bool:
        idx = self._hash(key)
        entry = self._buckets[idx]
        prev = None
        while entry:
            if entry.key == key:
                if prev: prev.next = entry.next
                else: self._buckets[idx] = entry.next
                self._size -= 1
                return True
            prev = entry
            entry = entry.next
        return False

    def size(self) -> int:
        return self._size
