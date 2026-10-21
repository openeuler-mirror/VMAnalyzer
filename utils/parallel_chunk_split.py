"""Split a workload into balanced chunks for parallel collectors.

Naive slicing by count produces imbalance when probe costs vary widely.
Weighted splitting by estimated cost keeps wall-clock time roughly even
across workers.
"""

import logging
from typing import Dict, Iterable, List, Sequence, Tuple

LOG = logging.getLogger(__name__)


def split_even(items: Sequence, workers: int) -> List[Sequence]:
    """Split a sequence into at most *workers* contiguous slices."""
    if workers <= 0:
        raise ValueError("workers must be positive")
    if not items:
        return []
    size = (len(items) + workers - 1) // workers
    return [items[index:index + size] for index in range(0, len(items), size)]


def split_weighted(items: Iterable[Tuple[str, float]], workers: int) -> List[List[str]]:
    """Assign items to the worker with the least accumulated cost."""
    if workers <= 0:
        raise ValueError("workers must be positive")
    ordered = sorted(items, key=lambda item: item[1], reverse=True)
    buckets: List[List[str]] = [[] for _ in range(workers)]
    loads = [0.0] * workers
    for name, cost in ordered:
        target = min(range(workers), key=lambda index: loads[index])
        buckets[target].append(name)
        loads[target] += max(0.0, float(cost))
    LOG.debug("split %d item(s) across %d worker(s), max load %.2f",
              len(ordered), workers, max(loads) if loads else 0.0)
    return buckets


def load_report(buckets: List[List[str]], costs: Dict[str, float]) -> Dict[str, float]:
    """Return the total cost assigned to each worker index."""
    return {"worker-{}".format(index): round(sum(costs.get(name, 0.0) for name in names), 2)
            for index, names in enumerate(buckets)}


__all__ = ["split_even", "split_weighted", "load_report"]
