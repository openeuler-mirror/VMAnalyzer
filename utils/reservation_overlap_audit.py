"""Audit reservations for pairwise time overlaps.

Reservations are sorted by start time so that a single sweep can flag every
conflicting pair: for each reservation only the following ones whose start is
before its end need checking.  Summary helpers count conflicts per resource.
"""

import logging
from typing import Dict, Iterable, List, Tuple

LOG = logging.getLogger(__name__)

Reservation = Tuple[str, float, float]


def find_conflicts(reservations: Iterable[Reservation]) -> List[Tuple[str, str]]:
    """Return id pairs whose time windows overlap."""
    ordered = sorted(reservations, key=lambda item: (item[1], item[2]))
    conflicts: List[Tuple[str, str]] = []
    for index, (id_first, _, end_first) in enumerate(ordered):
        for id_second, start_second, _ in ordered[index + 1:]:
            if start_second >= end_first:
                break
            conflicts.append((id_first, id_second))
    LOG.debug("found %d conflicting pairs", len(conflicts))
    return conflicts


def conflict_counts(reservations: Iterable[Reservation]) -> Dict[str, int]:
    """Count how many conflicts each reservation participates in."""
    counts: Dict[str, int] = {}
    for first, second in find_conflicts(reservations):
        counts[first] = counts.get(first, 0) + 1
        counts[second] = counts.get(second, 0) + 1
    return counts


def conflict_ratio(reservations: Iterable[Reservation]) -> float:
    """Return the proportion of reservation pairs that conflict."""
    materialised = list(reservations)
    total_pairs = len(materialised) * (len(materialised) - 1) // 2
    if total_pairs == 0:
        return 0.0
    return len(find_conflicts(materialised)) / total_pairs


__all__ = ["find_conflicts", "conflict_counts", "conflict_ratio"]
