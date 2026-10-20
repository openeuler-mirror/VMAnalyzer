"""Daylight saving awareness checks.

Detects whether an interval straddles a clock shift so schedulers can avoid
double counting or missing an hour when adding durations to wall clock times.
"""
import logging

LOG = logging.getLogger(__name__)


def utcoffset_seconds(moment):
    """Return the UTC offset of an aware datetime in seconds."""
    offset = moment.utcoffset()
    if offset is None:
        return 0
    return int(offset.total_seconds())


def crosses_dst(start, end):
    """Report whether the UTC offset changes between two instants."""
    if start.tzinfo is None or end.tzinfo is None:
        LOG.debug("naive datetimes supplied, assuming no shift")
        return False
    return utcoffset_seconds(start) != utcoffset_seconds(end)


def shift_delta(start, end):
    """Return the offset change in seconds between two instants."""
    return utcoffset_seconds(end) - utcoffset_seconds(start)


__all__ = ["utcoffset_seconds", "crosses_dst", "shift_delta"]
