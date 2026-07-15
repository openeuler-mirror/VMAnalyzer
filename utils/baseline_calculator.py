#!/usr/bin/env python3
"""Calculate metric baselines for comparison."""
from typing import Dict, List, Optional

class BaselineCalculator:
    """Calculates and stores baseline values for metrics."""

    def __init__(self):
        self._baselines: Dict[str, dict] = {}

    def calculate(self, metric: str, values: List[float]) -> dict:
        """Calculate baseline statistics from historical data."""
        if not values:
            raise ValueError("Cannot calculate baseline from empty data")
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        baseline = {
            "mean": sum(values) / n,
            "median": sorted_vals[n // 2],
            "p95": sorted_vals[int(n * 0.95)] if n > 1 else sorted_vals[0],
            "min": min(values),
            "max": max(values),
            "std": (sum((x - sum(values) / n) ** 2 for x in values) / n) ** 0.5,
        }
        self._baselines[metric] = baseline
        return baseline

    def get(self, metric: str) -> Optional[dict]:
        """Get stored baseline for a metric."""
        return self._baselines.get(metric)

    def deviation(self, metric: str, value: float) -> Optional[float]:
        """Calculate deviation from baseline mean."""
        bl = self._baselines.get(metric)
        if not bl:
            return None
        return value - bl["mean"]

    def is_anomalous(self, metric: str, value: float,
                     threshold: float = 2.0) -> bool:
        """Check if value deviates significantly from baseline."""
        bl = self._baselines.get(metric)
        if not bl or bl["std"] == 0:
            return False
        z = abs(value - bl["mean"]) / bl["std"]
        return z > threshold
