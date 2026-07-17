#!/usr/bin/env python3
"""Linear trend analysis for metric time series."""
from typing import List, Tuple

class TrendAnalyzer:
    """Analyzes linear trends in metric data using least squares."""

    def __init__(self):
        self._data: List[Tuple[float, float]] = []

    def add_point(self, x: float, y: float) -> None:
        """Add a data point."""
        self._data.append((x, y))

    def calculate(self) -> dict:
        """Calculate linear regression (slope, intercept, r_squared)."""
        n = len(self._data)
        if n < 2:
            return {"slope": 0, "intercept": 0, "r_squared": 0}
        xs = [d[0] for d in self._data]
        ys = [d[1] for d in self._data]
        mean_x = sum(xs) / n
        mean_y = sum(ys) / n
        num = sum((x - mean_x) * (y - mean_y) for x, y in self._data)
        den_x = sum((x - mean_x) ** 2 for x in xs)
        den_y = sum((y - mean_y) ** 2 for y in ys)
        slope = num / den_x if den_x else 0
        intercept = mean_y - slope * mean_x
        r_sq = (num ** 2) / (den_x * den_y) if den_x and den_y else 0
        return {"slope": slope, "intercept": intercept, "r_squared": r_sq}

    def predict(self, x: float) -> float:
        """Predict y value for given x using fitted line."""
        r = self.calculate()
        return r["slope"] * x + r["intercept"]

    def is_increasing(self) -> bool:
        """Check if trend is increasing."""
        return self.calculate()["slope"] > 0

    def clear(self) -> None:
        """Clear all data points."""
        self._data.clear()
