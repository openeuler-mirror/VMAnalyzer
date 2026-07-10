#!/usr/bin/env python3
"""Statistical calculator for descriptive statistics."""
import math
from typing import List, Optional, Dict

class StatCalculator:
    def __init__(self, data: List[float] = None):
        self._data = sorted(data) if data else []

    def add(self, val: float) -> None:
        self._data.append(val)
        self._data.sort()

    def mean(self) -> float:
        return sum(self._data) / len(self._data) if self._data else 0

    def median(self) -> float:
        n = len(self._data)
        if n == 0: return 0
        if n % 2: return self._data[n//2]
        return (self._data[n//2-1] + self._data[n//2]) / 2

    def mode(self) -> List[float]:
        from collections import Counter
        c = Counter(self._data)
        max_count = max(c.values()) if c else 0
        return [k for k, v in c.items() if v == max_count]

    def variance(self) -> float:
        n = len(self._data)
        if n < 2: return 0
        m = self.mean()
        return sum((x - m) ** 2 for x in self._data) / (n - 1)

    def std_dev(self) -> float:
        return math.sqrt(self.variance())

    def percentile(self, p: float) -> float:
        if not self._data: return 0
        idx = (p / 100) * (len(self._data) - 1)
        lo = int(math.floor(idx))
        hi = int(math.ceil(idx))
        if lo == hi: return self._data[lo]
        return self._data[lo] + (self._data[hi] - self._data[lo]) * (idx - lo)

    def summary(self) -> Dict[str, float]:
        return {
            "count": len(self._data), "mean": self.mean(),
            "median": self.median(), "std_dev": self.std_dev(),
            "min": min(self._data) if self._data else 0,
            "max": max(self._data) if self._data else 0,
            "q1": self.percentile(25), "q3": self.percentile(75)
        }
