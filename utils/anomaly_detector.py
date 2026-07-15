#!/usr/bin/env python3
"""Statistical anomaly detection using Z-score and IQR methods for VM metrics."""
import math
from typing import Dict, List, Optional, Tuple

class AnomalyDetector:
    """Detects anomalies in metric streams using statistical methods."""

    def __init__(self, method: str = "zscore", threshold: float = 3.0):
        self._method = method
        self._threshold = threshold
        self._models: Dict[str, dict] = {}

    def fit(self, metric_name: str, values: List[float]) -> None:
        """Build a statistical model from historical data."""
        if len(values) < 4:
            raise ValueError("Need at least 4 samples to fit")
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std = math.sqrt(variance) if variance > 0 else 1e-10
        sorted_vals = sorted(values)
        q1 = self._percentile(sorted_vals, 25)
        q3 = self._percentile(sorted_vals, 75)
        iqr = q3 - q1
        self._models[metric_name] = {
            "mean": mean,
            "std": std,
            "q1": q1,
            "q3": q3,
            "iqr": iqr if iqr > 0 else 1e-10,
            "lower_bound": q1 - 1.5 * (iqr if iqr > 0 else 1e-10),
            "upper_bound": q3 + 1.5 * (iqr if iqr > 0 else 1e-10),
            "count": len(values),
        }

    def detect(self, metric_name: str, value: float) -> bool:
        """Check if a value is anomalous."""
        if metric_name not in self._models:
            raise KeyError(f"Metric '{metric_name}' not fitted")
        model = self._models[metric_name]
        if self._method == "zscore":
            z = abs(value - model["mean"]) / model["std"]
            return z > self._threshold
        else:
            return value < model["lower_bound"] or value > model["upper_bound"]

    def detect_batch(self, metric_name: str, values: List[float]) -> List[bool]:
        """Detect anomalies in a batch of values."""
        return [self.detect(metric_name, v) for v in values]

    def score(self, metric_name: str, value: float) -> float:
        """Return an anomaly score (higher = more anomalous)."""
        if metric_name not in self._models:
            raise KeyError(f"Metric '{metric_name}' not fitted")
        model = self._models[metric_name]
        if self._method == "zscore":
            return abs(value - model["mean"]) / model["std"]
        else:
            if value < model["lower_bound"]:
                return (model["lower_bound"] - value) / model["iqr"]
            elif value > model["upper_bound"]:
                return (value - model["upper_bound"]) / model["iqr"]
            return 0.0

    def get_model(self, metric_name: str) -> Optional[dict]:
        """Return the fitted model parameters."""
        return self._models.get(metric_name)

    @staticmethod
    def _percentile(sorted_vals: List[float], pct: float) -> float:
        """Calculate percentile from sorted values."""
        if not sorted_vals:
            return 0.0
        k = (len(sorted_vals) - 1) * pct / 100.0
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return sorted_vals[int(k)]
        d = k - f
        return sorted_vals[f] * (1 - d) + sorted_vals[c] * d
