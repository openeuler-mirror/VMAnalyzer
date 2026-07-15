#!/usr/bin/env python3
"""Counting bloom filter for frequency estimation."""
import hashlib
from typing import List

class BloomCounter:
    """A counting bloom filter for approximate frequency counting."""

    def __init__(self, capacity: int = 1000, error_rate: float = 0.01):
        self._size = int(-capacity * (error_rate ** -1) / 0.69) + 1
        self._size = max(self._size, 8)
        self._counts = [0] * self._size
        self._num_hashes = max(int(0.69 * self._size / capacity), 1)
        self._added = 0

    def _hashes(self, item: str) -> List[int]:
        """Generate hash positions for an item."""
        positions = []
        for i in range(self._num_hashes):
            h = hashlib.md5(f"{item}{i}".encode()).hexdigest()
            positions.append(int(h, 16) % self._size)
        return positions

    def add(self, item: str) -> None:
        """Add an item to the filter."""
        for pos in self._hashes(item):
            self._counts[pos] += 1
        self._added += 1

    def estimate(self, item: str) -> int:
        """Estimate the frequency of an item."""
        counts = [self._counts[p] for p in self._hashes(item)]
        return min(counts) if counts else 0

    def remove(self, item: str) -> bool:
        """Decrement count for an item."""
        if self.estimate(item) == 0:
            return False
        for pos in self._hashes(item):
            if self._counts[pos] > 0:
                self._counts[pos] -= 1
        return True

    def __len__(self) -> int:
        return self._added
