"""Interval job packing choosing the largest non-overlapping set.

Sorting jobs by finish time and greedily accepting any job that starts after
the last accepted finish is optimal for maximising the number of packed jobs
on a single machine.
"""

import logging
from typing import Iterable, List, Tuple

LOG = logging.getLogger(__name__)

Job = Tuple[float, float]


def select_jobs(jobs: Iterable[Job]) -> List[Job]:
    """Pick the largest set of mutually non-overlapping jobs."""
    ordered = sorted(jobs, key=lambda job: (job[1], job[0]))
    chosen: List[Job] = []
    last_finish = float("-inf")
    for start, finish in ordered:
        if start >= last_finish:
            chosen.append((start, finish))
            last_finish = finish
    LOG.debug("packed %d of %d jobs", len(chosen), len(ordered))
    return chosen


def max_jobs(jobs: Iterable[Job]) -> int:
    """Return the maximum number of non-overlapping jobs."""
    return len(select_jobs(jobs))


def busy_fraction(jobs: Iterable[Job], horizon: float) -> float:
    """Return the share of a horizon occupied by the selected jobs."""
    chosen = select_jobs(jobs)
    busy = sum(finish - start for start, finish in chosen)
    return busy / horizon if horizon else 0.0


def uncovered(jobs: Iterable[Job], horizon: float) -> float:
    """Return how much of the horizon is left idle by the packed schedule."""
    return max(0.0, horizon - sum(finish - start for start, finish in select_jobs(jobs)))


__all__ = ["select_jobs", "max_jobs", "busy_fraction", "uncovered"]
