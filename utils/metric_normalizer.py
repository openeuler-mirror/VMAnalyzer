#!/usr/bin/env python3
"""Metric normalization utility for scaling VM performance data to standard ranges."""
import math
from typing import Dict, List, Optional, Tuple

class MetricNormalizer:
    """Normalizes metric values using min-max or z-score scaling."""

    def __init__(self, method: str = "minmax"):
        self._method = method
        self._stats: Dict[str, Tuple[float, float, float, float]] = {}

    def fit(self, metric_name: str, values: List[float]) -> None:
        """Compute normalization parameters from training data."""
        if not values:
            raise ValueError("Cannot fit on empty data")
        if self._method == "minmax":
            min_val = min(values)
            max_val = max(values)
            mean = sum(values) / len(values)
            self._stats[metric_name] = (min_val, max_val, mean, 0.0)
        elif self._method == "zscore":
            mean = sum(values) / len(values)
            variance = sum((x - mean) ** 2 for x in values) / len(values)
            std = math.sqrt(variance) if variance > 0 else 1.0
            self._stats[metric_name] = (0.0, 0.0, mean, std)
        else:
            raise ValueError(f"Unknown method: {self._method}")

    def transform(self, metric_name: str, value: float) -> float:
        """Transform a single value using fitted parameters."""
        if metric_name not in self._stats:
            raise KeyError(f"Metric '{metric_name}' not fitted")
        min_val, max_val, mean, std = self._stats[metric_name]
        if self._method == "minmax":
            range_val = max_val - min_val
            if range_val == 0:
                return 0.0
            return (value - min_val) / range_val
        else:
            return (value - mean) / std if std > 0 else 0.0

    def fit_transform(self, metric_name: str, values: List[float]) -> List[float]:
        """Fit and transform in one step."""
        self.fit(metric_name, values)
        return [self.transform(metric_name, v) for v in values]

    def denormalize(self, metric_name: str, normalized: float) -> float:
        """Reverse the normalization to get original value."""
        if metric_name not in self._stats:
            raise KeyError(f"Metric '{metric_name}' not fitted")
        min_val, max_val, mean, std = self._stats[metric_name]
        if self._method == "minmax":
            return normalized * (max_val - min_val) + min_val
        else:
            return normalized * std + mean

    def get_stats(self, metric_name: str) -> Optional[Dict[str, float]]:
        """Return fitted statistics for a metric."""
        if metric_name not in self._stats:
            return None
        min_val, max_val, mean, std = self._stats[metric_name]
        return {"min": min_val, "max": max_val, "mean": mean, "std": std}

    def is_fitted(self, metric_name: str) -> bool:
        """Check if a metric has been fitted."""
        return metric_name in self._stats
