#!/usr/bin/env python3
"""Word frequency counter with statistics."""
import re
from collections import Counter
from typing import Dict, List, Tuple

class WordCounter:
    def __init__(self):
        self._counter: Counter = Counter()
        self._total = 0

    def feed(self, text: str) -> None:
        words = re.findall(r"\b\w+\b", text.lower())
        self._counter.update(words)
        self._total += len(words)

    def most_common(self, n: int = 10) -> List[Tuple[str, int]]:
        return self._counter.most_common(n)

    def frequency(self, word: str) -> float:
        if self._total == 0:
            return 0.0
        return self._counter.get(word.lower(), 0) / self._total

    def unique_count(self) -> int:
        return len(self._counter)

    def total_count(self) -> int:
        return self._total

    def get_all(self) -> Dict[str, int]:
        return dict(self._counter)

    def filter_min(self, min_count: int) -> Dict[str, int]:
        return {w: c for w, c in self._counter.items() if c >= min_count}

    def merge(self, other: "WordCounter") -> None:
        self._counter.update(other._counter)
        self._total += other._total

    def reset(self) -> None:
        self._counter.clear()
        self._total = 0
