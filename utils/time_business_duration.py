"""Measure how much of an interval falls inside business hours.

Maintenance windows often target weekday office hours, but incident
timelines are recorded in wall-clock time.  Subtracting the out-of-hours
portion gives an honest service impact figure.
"""

import logging
from datetime import datetime, time, timedelta
from typing import Tuple

LOG = logging.getLogger(__name__)


def _combine(day, moment: time) -> datetime:
    """Attach a clock time to a date, keeping the date's timezone info."""
    return datetime.combine(day, moment, tzinfo=day.tzinfo)


def business_duration(start: datetime, end: datetime,
                      work_start: time = time(9, 0),
                      work_end: time = time(18, 0),
                      weekdays: Tuple[int, ...] = (0, 1, 2, 3, 4)) -> timedelta:
    """Return the part of ``[start, end)`` spent on configured workdays."""
    if end <= start:
        LOG.debug("empty or reversed interval, duration is zero")
        return timedelta(0)
    total = timedelta(0)
    cursor = start
    while cursor.date() <= end.date():
        if cursor.weekday() in weekdays:
            window_start = max(cursor, _combine(cursor, work_start))
            window_end = min(end, _combine(cursor, work_end))
            if window_end > window_start:
                total += window_end - window_start
        cursor = _combine(cursor.date() + timedelta(days=1), time(0, 0))
    LOG.debug("business duration %s for interval %s..%s", total, start, end)
    return total


def business_ratio(start: datetime, end: datetime) -> float:
    """Return the business-hours share of the total interval."""
    total = end - start
    if total.total_seconds() <= 0:
        return 0.0
    return round(business_duration(start, end).total_seconds() / total.total_seconds(), 4)


__all__ = ["business_duration", "business_ratio"]
