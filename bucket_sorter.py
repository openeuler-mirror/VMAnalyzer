"""Bucket sorter for categorizing metric values into named ranges."""

from typing import Dict, List, Optional, Tuple


class BucketSorter:
    """Sorts values into configurable named buckets based on boundaries."""

    def __init__(self) -> None:
        self._buckets: Dict[str, Tuple[float, float]] = {}
        self._ordered_names: List[str] = []

    def define_bucket(self, name: str, low: float, high: float) -> None:
        if name in self._buckets:
            self._ordered_names.remove(name)
        self._buckets[name] = (low, high)
        self._ordered_names.append(name)
        self._ordered_names.sort(key=lambda n: self._buckets[n][0])

    def classify(self, value: float) -> Optional[str]:
        for name in self._ordered_names:
            low, high = self._buckets[name]
            if low <= value < high:
                return name
        return None

    def classify_all(self, values: List[float]) -> Dict[str, List[float]]:
        result: Dict[str, List[float]] = {name: [] for name in self._ordered_names}
        result["_unclassified"] = []
        for v in values:
            bucket = self.classify(v)
            if bucket:
                result[bucket].append(v)
            else:
                result["_unclassified"].append(v)
        return result

    def distribution(self, values: List[float]) -> Dict[str, int]:
        classified = self.classify_all(values)
        return {k: len(v) for k, v in classified.items()}

    def bucket_names(self) -> List[str]:
        return list(self._ordered_names)

    def bucket_range(self, name: str) -> Optional[Tuple[float, float]]:
        return self._buckets.get(name)

    def remove_bucket(self, name: str) -> None:
        if name in self._buckets:
            del self._buckets[name]
            self._ordered_names.remove(name)

    def clear(self) -> None:
        self._buckets.clear()
        self._ordered_names.clear()
