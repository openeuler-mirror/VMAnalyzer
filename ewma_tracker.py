"""Exponentially weighted moving average tracker for metric smoothing."""

from typing import Dict, List, Optional


class EwmaTracker:
    """Tracks EWMA across multiple metric keys simultaneously."""

    def __init__(self, alpha: float = 0.2) -> None:
        if not 0 < alpha <= 1:
            raise ValueError("alpha must be in (0, 1]")
        self._alpha = alpha
        self._values: Dict[str, float] = {}

    def update(self, key: str, value: float) -> float:
        if key not in self._values:
            self._values[key] = value
        else:
            old = self._values[key]
            self._values[key] = self._alpha * value + (1 - self._alpha) * old
        return self._values[key]

    def get(self, key: str) -> Optional[float]:
        return self._values.get(key)

    def batch_update(self, updates: Dict[str, float]) -> Dict[str, float]:
        result = {}
        for key, val in updates.items():
            result[key] = self.update(key, val)
        return result

    def keys(self) -> List[str]:
        return list(self._values.keys())

    def snapshot(self) -> Dict[str, float]:
        return dict(self._values)

    def remove(self, key: str) -> None:
        self._values.pop(key, None)

    def clear(self) -> None:
        self._values.clear()

    @property
    def alpha(self) -> float:
        return self._alpha
