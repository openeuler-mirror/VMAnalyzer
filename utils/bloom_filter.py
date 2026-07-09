#!/usr/bin/env python3
"""Bloom filter for probabilistic membership testing."""
import hashlib
from typing import List

class BloomFilter:
    def __init__(self, size: int = 1000, hash_count: int = 3):
        self._size = size
        self._hash_count = hash_count
        self._bits = [False] * size

    def _hashes(self, item: str) -> List[int]:
        result = []
        for i in range(self._hash_count):
            h = hashlib.md5(f"{i}:{item}".encode()).hexdigest()
            result.append(int(h, 16) % self._size)
        return result

    def add(self, item: str) -> None:
        for h in self._hashes(item):
            self._bits[h] = True

    def might_contain(self, item: str) -> bool:
        return all(self._bits[h] for h in self._hashes(item))

    def clear(self) -> None:
        self._bits = [False] * self._size

    def estimated_count(self) -> float:
        set_bits = sum(self._bits)
        if set_bits == 0:
            return 0.0
        import math
        return -(self._size / self._hash_count) * math.log(1 - set_bits / self._size)
