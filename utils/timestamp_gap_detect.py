"""Detect gaps in a stream of timestamps.

Flags missing samples by comparing the spacing between consecutive timestamps
against the expected cadence and a tolerance multiplier.
"""
import logging

LOG = logging.getLogger(__name__)


def gaps(timestamps, expected_interval, tolerance=2.0):
    """Return (previous, current) pairs whose spacing looks like a gap."""
    ordered = sorted(timestamps)
    limit = expected_interval * tolerance
    found = []
    for previous, current in zip(ordered, ordered[1:]):
        if current - previous > limit:
            found.append((previous, current))
    return found


def largest_gap(timestamps):
    """Return the widest spacing between consecutive timestamps."""
    ordered = sorted(timestamps)
    if len(ordered) < 2:
        return 0
    return max(b - a for a, b in zip(ordered, ordered[1:]))


def coverage_ratio(timestamps, expected_interval):
    """Return the share of expected samples actually present."""
    ordered = sorted(timestamps)
    if len(ordered) < 2 or expected_interval <= 0:
        return 0.0
    span = ordered[-1] - ordered[0]
    expected = span / float(expected_interval) + 1
    return round(len(ordered) / expected, 4)


__all__ = ["gaps", "largest_gap", "coverage_ratio"]
