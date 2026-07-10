#!/usr/bin/env python3
"""Metrics collector for counters, gauges, and histograms."""
from typing import Dict, List, Optional, Any
import threading
import time
from collections import defaultdict

class Counter:
    def __init__(self, name: str, description: str = ""):
        self._name = name
        self._desc = description
        self._value = 0
        self._lock = threading.Lock()
        self._labels: Dict[str, int] = defaultdict(int)

    def inc(self, amount: int = 1, label: str = "") -> None:
        with self._lock:
            self._value += amount
            if label:
                self._labels[label] += amount

    @property
    def value(self) -> int:
        return self._value

    @property
    def name(self) -> str:
        return self._name

    def labels(self) -> Dict[str, int]:
        return dict(self._labels)

    def reset(self) -> None:
        with self._lock:
            self._value = 0
            self._labels.clear()

class Gauge:
    def __init__(self, name: str, description: str = ""):
        self._name = name
        self._desc = description
        self._value = 0.0
        self._lock = threading.Lock()

    def set(self, value: float) -> None:
        with self._lock:
            self._value = value

    def inc(self, amount: float = 1.0) -> None:
        with self._lock:
            self._value += amount

    def dec(self, amount: float = 1.0) -> None:
        with self._lock:
            self._value -= amount

    @property
    def value(self) -> float:
        return self._value

    @property
    def name(self) -> str:
        return self._name

class Histogram:
    def __init__(self, name: str, buckets: Optional[List[float]] = None):
        self._name = name
        self._buckets = sorted(buckets or [0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10])
        self._counts: List[int] = [0] * len(self._buckets)
        self._sum = 0.0
        self._count = 0
        self._lock = threading.Lock()
        self._values: List[float] = []

    def observe(self, value: float) -> None:
        with self._lock:
            self._sum += value
            self._count += 1
            self._values.append(value)
            if len(self._values) > 10000:
                self._values = self._values[-5000:]
            for i, b in enumerate(self._buckets):
                if value <= b:
                    self._counts[i] += 1

    @property
    def count(self) -> int:
        return self._count

    @property
    def sum(self) -> float:
        return self._sum

    def percentile(self, p: float) -> float:
        with self._lock:
            if not self._values:
                return 0.0
            sorted_vals = sorted(self._values)
            idx = int(len(sorted_vals) * p / 100)
            return sorted_vals[min(idx, len(sorted_vals) - 1)]

    def mean(self) -> float:
        return self._sum / self._count if self._count > 0 else 0.0

class MetricsCollector:
    def __init__(self):
        self._counters: Dict[str, Counter] = {}
        self._gauges: Dict[str, Gauge] = {}
        self._histograms: Dict[str, Histogram] = {}
        self._lock = threading.Lock()

    def counter(self, name: str, desc: str = "") -> Counter:
        with self._lock:
            if name not in self._counters:
                self._counters[name] = Counter(name, desc)
            return self._counters[name]

    def gauge(self, name: str, desc: str = "") -> Gauge:
        with self._lock:
            if name not in self._gauges:
                self._gauges[name] = Gauge(name, desc)
            return self._gauges[name]

    def histogram(self, name: str, buckets: Optional[List[float]] = None) -> Histogram:
        with self._lock:
            if name not in self._histograms:
                self._histograms[name] = Histogram(name, buckets)
            return self._histograms[name]

    def export(self) -> Dict[str, Any]:
        return {
            "counters": {n: {"value": c.value, "labels": c.labels()} for n, c in self._counters.items()},
            "gauges": {n: g.value for n, g in self._gauges.items()},
            "histograms": {n: {"count": h.count, "sum": h.sum, "mean": h.mean(),
                               "p50": h.percentile(50), "p99": h.percentile(99)}
                          for n, h in self._histograms.items()},
        }

    def reset(self) -> None:
        with self._lock:
            for c in self._counters.values(): c.reset()
            for g in self._gauges.values(): g.set(0)
            self._counters.clear()
            self._gauges.clear()
            self._histograms.clear()
