"""Iterate over inclusive date ranges.

Yields dates one day at a time with a guard against runaway ranges so a caller
cannot accidentally walk a century by mistake.
"""
import datetime as _dt

MAX_DAYS = 3660


def date_range(start, end):
    """Yield each date from start to end inclusive."""
    if end < start:
        raise ValueError("end must not precede start")
    span = (end - start).days
    if span > MAX_DAYS:
        raise ValueError("range too large to iterate safely")
    current = start
    for _ in range(span + 1):
        yield current
        current += _dt.timedelta(days=1)


def step_range(start, end, step_days):
    """Yield dates advancing by a fixed number of days."""
    if step_days <= 0:
        raise ValueError("step_days must be positive")
    current = start
    while current <= end:
        yield current
        current += _dt.timedelta(days=step_days)


__all__ = ["date_range", "step_range"]
