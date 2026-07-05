"""Duration ring buffer."""

from __future__ import annotations

from collections import deque


class DurationRingBuffer:
    def __init__(self, maxlen: int = 100):
        self._items = deque(maxlen=maxlen)

    def append(self, value: float) -> None:
        self._items.append(value)

    def values(self) -> list[float]:
        return list(self._items)

