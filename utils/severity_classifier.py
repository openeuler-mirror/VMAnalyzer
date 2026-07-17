#!/usr/bin/env python3
"""Classify alert severity levels based on metric thresholds."""
from typing import Optional

class SeverityClassifier:
    """Classifies metric values into severity levels."""

    def __init__(self):
        self._rules = []

    def add_rule(self, metric: str, warning: float,
                 critical: float, fatal: float = None) -> None:
        """Add a severity classification rule."""
        self._rules.append({
            "metric": metric,
            "warning": warning,
            "critical": critical,
            "fatal": fatal if fatal else critical * 1.5,
        })

    def classify(self, metric: str, value: float) -> str:
        """Classify a metric value into severity."""
        for rule in self._rules:
            if rule["metric"] == metric:
                if value >= rule["fatal"]:
                    return "fatal"
                if value >= rule["critical"]:
                    return "critical"
                if value >= rule["warning"]:
                    return "warning"
                return "normal"
        return "unknown"

    def get_thresholds(self, metric: str) -> Optional[dict]:
        """Get thresholds for a metric."""
        for rule in self._rules:
            if rule["metric"] == metric:
                return rule
        return None
