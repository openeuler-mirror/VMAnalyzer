"""Jaccard index and numeric set similarity helpers."""
import logging

LOG = logging.getLogger(__name__)


def jaccard(left, right):
    """Return the Jaccard index of two iterables in the 0..1 range."""
    a = set(left or [])
    b = set(right or [])
    if not a and not b:
        return 1.0
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / float(len(union))


def jaccard_distance(left, right):
    """Return one minus the Jaccard index of two iterables."""
    return 1.0 - jaccard(left, right)


def tolerance_intersection(left, right, tolerance):
    """Return the fraction of left values matched within tolerance in right."""
    source = [float(v) for v in left or []]
    target = [float(v) for v in right or []]
    if not source:
        return 0.0
    matches = sum(1 for value in source
                  if any(abs(value - other) <= tolerance for other in target))
    return matches / float(len(source))


__all__ = ['jaccard', 'jaccard_distance', 'tolerance_intersection']
