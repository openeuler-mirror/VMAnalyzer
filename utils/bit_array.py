#!/usr/bin/env python3
"""Bit array for compact boolean storage."""
from typing import List

class BitArray:
    def __init__(self, size: int):
        self._size = size
        self._bits = [0] * ((size + 63) // 64)

    def set(self, index: int, value: bool = True) -> None:
        if 0 <= index < self._size:
            word = index // 64
            bit = index % 64
            if value:
                self._bits[word] |= (1 << bit)
            else:
                self._bits[word] &= ~(1 << bit)

    def get(self, index: int) -> bool:
        if 0 <= index < self._size:
            word = index // 64
            bit = index % 64
            return bool(self._bits[word] & (1 << bit))
        return False

    def toggle(self, index: int) -> None:
        if 0 <= index < self._size:
            word = index // 64
            bit = index % 64
            self._bits[word] ^= (1 << bit)

    def count_set(self) -> int:
        return sum(bin(w).count("1") for w in self._bits)

    def clear_all(self) -> None:
        self._bits = [0] * len(self._bits)

    def set_all(self) -> None:
        self._bits = [0xFFFFFFFFFFFFFFFF] * len(self._bits)

    def size(self) -> int:
        return self._size
