#!/usr/bin/env python3
"""Filter metrics by name patterns for selective collection."""
import re
from typing import Dict, List, Set

class MetricFilter:
    """Filters metrics based on include/exclude patterns."""

    def __init__(self):
        self._include: Set[str] = set()
        self._exclude: Set[str] = set()
        self._include_regex: List[re.Pattern] = []
        self._exclude_regex: List[re.Pattern] = []

    def add_include(self, pattern: str) -> None:
        """Add an include pattern."""
        self._include.add(pattern)
        self._include_regex.append(re.compile(pattern))

    def add_exclude(self, pattern: str) -> None:
        """Add an exclude pattern."""
        self._exclude.add(pattern)
        self._exclude_regex.append(re.compile(pattern))

    def matches(self, metric_name: str) -> bool:
        """Check if a metric should be included."""
        if any(r.search(metric_name) for r in self._exclude_regex):
            return False
        if not self._include_regex:
            return True
        return any(r.search(metric_name) for r in self._include_regex)

    def filter_metrics(self, metrics: Dict[str, float]) -> Dict[str, float]:
        """Filter a dictionary of metrics."""
        return {k: v for k, v in metrics.items() if self.matches(k)}
