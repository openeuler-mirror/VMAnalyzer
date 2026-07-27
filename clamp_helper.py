"""Value clamp helper for enforcing safe metric ranges."""

from typing import Optional, Tuple


class ClampHelper:
    """Clamps values to configurable per-key min/max ranges."""

    def __init__(self) -> None:
        self._ranges: dict = {}

    def set_range(self, key: str, min_val: float, max_val: float) -> None:
        if min_val > max_val:
            raise ValueError("min_val must not exceed max_val")
        self._ranges[key] = (min_val, max_val)

    def get_range(self, key: str) -> Optional[Tuple[float, float]]:
        return self._ranges.get(key)

    def clamp(self, key: str, value: float) -> float:
        rng = self._ranges.get(key)
        if rng is None:
            return value
        lo, hi = rng
        return max(lo, min(hi, value))

    def clamp_many(self, key: str, values: list) -> list:
        return [self.clamp(key, v) for v in values]

    def is_in_range(self, key: str, value: float) -> bool:
        rng = self._ranges.get(key)
        if rng is None:
            return True
        lo, hi = rng
        return lo <= value <= hi

    def violations(self, key: str, values: list) -> list:
        return [v for v in values if not self.is_in_range(key, v)]

    def remove_range(self, key: str) -> None:
        self._ranges.pop(key, None)

    def keys(self) -> list:
        return list(self._ranges.keys())

    def clear(self) -> None:
        self._ranges.clear()
