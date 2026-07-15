#!/usr/bin/env python3
"""Simple metric forecasting using moving averages."""
from collections import deque
from typing import Deque, List

class ForecastEstimator:
    """Forecasts future metric values using moving average."""

    def __init__(self, window_size: int = 10):
        self._window = window_size
        self._history: Deque[float] = deque(maxlen=window_size)

    def observe(self, value: float) -> None:
        """Add an observation."""
        self._history.append(value)

    def forecast(self, steps: int = 1) -> List[float]:
        """Forecast future values using linear extrapolation."""
        data = list(self._history)
        if len(data) < 2:
            return [data[-1] if data else 0.0] * steps
        avg = sum(data) / len(data)
        diff = data[-1] - data[0]
        trend = diff / len(data)
        return [avg + trend * (i + 1) for i in range(steps)]

    def confidence(self) -> float:
        """Return confidence score based on data variance."""
        data = list(self._history)
        if len(data) < 2:
            return 0.0
        mean = sum(data) / len(data)
        variance = sum((x - mean) ** 2 for x in data) / len(data)
        return max(0.0, 1.0 - variance / (mean ** 2)) if mean else 0.0
