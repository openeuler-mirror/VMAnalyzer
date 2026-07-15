#!/usr/bin/env python3
"""Pattern matching for metric value sequences."""
from typing import List, Optional

class PatternMatcher:
    """Matches predefined patterns in metric sequences."""

    def __init__(self):
        self._patterns: dict = {}

    def register(self, name: str, sequence: List[float],
                 tolerance: float = 0.1) -> None:
        """Register a named pattern to match against."""
        self._patterns[name] = {"sequence": sequence, "tolerance": tolerance}

    def match(self, data: List[float]) -> Optional[str]:
        """Find the first matching pattern in data."""
        for name, pat in self._patterns.items():
            seq = pat["sequence"]
            tol = pat["tolerance"]
            if self._contains_pattern(data, seq, tol):
                return name
        return None

    def _contains_pattern(self, data: List[float], seq: List[float],
                          tol: float) -> bool:
        if len(seq) > len(data):
            return False
        for i in range(len(data) - len(seq) + 1):
            if all(abs(data[i + j] - seq[j]) <= tol for j in range(len(seq))):
                return True
        return False

    def list_patterns(self) -> List[str]:
        """Return all registered pattern names."""
        return list(self._patterns.keys())
