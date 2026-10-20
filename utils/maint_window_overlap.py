"""Detect overlapping maintenance windows.

Monitors two maintenance intervals for the same host and reports the overlap so
operators are warned before scheduling double disruption.
"""
import logging

LOG = logging.getLogger(__name__)


def overlaps(first, second):
    """Report whether two half-open (start, end) intervals overlap."""
    first_start, first_end = first
    second_start, second_end = second
    return first_start < second_end and second_start < first_end


def overlap_seconds(first, second):
    """Return the length of the shared interval, or zero."""
    start = max(first[0], second[0])
    end = min(first[1], second[1])
    return max(0, end - start)


def merge_windows(windows):
    """Merge a list of intervals into the minimal covering set."""
    ordered = sorted(windows)
    merged = []
    for start, end in ordered:
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


__all__ = ["overlaps", "overlap_seconds", "merge_windows"]
