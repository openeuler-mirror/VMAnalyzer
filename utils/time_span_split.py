"""Split a datetime range into consecutive day-aligned windows.

Daily retention jobs and per-day reports need boundaries that respect
calendar days instead of fixed 24 hour offsets.  The splitter keeps the
timezone of the input and always covers the full range exactly once.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Tuple

LOG = logging.getLogger(__name__)


def split_by_day(start: datetime, end: datetime) -> List[Tuple[datetime, datetime]]:
    """Return day-aligned ``(window_start, window_end)`` pairs covering the range."""
    if end <= start:
        LOG.debug("range is empty, no windows produced")
        return []
    windows: List[Tuple[datetime, datetime]] = []
    cursor = start
    while cursor < end:
        next_day = datetime(
            cursor.year, cursor.month, cursor.day, tzinfo=cursor.tzinfo
        ) + timedelta(days=1)
        boundary = min(next_day, end)
        windows.append((cursor, boundary))
        cursor = boundary
    LOG.debug("split range into %d day window(s)", len(windows))
    return windows


def split_fixed(start: datetime, end: datetime, seconds: int) -> List[Tuple[datetime, datetime]]:
    """Split the range into fixed length windows of *seconds* duration."""
    if seconds <= 0:
        raise ValueError("seconds must be positive")
    if end <= start:
        return []
    step = timedelta(seconds=seconds)
    windows: List[Tuple[datetime, datetime]] = []
    cursor = start
    while cursor < end:
        boundary = min(cursor + step, end)
        windows.append((cursor, boundary))
        cursor = boundary
    return windows


__all__ = ["split_by_day", "split_fixed"]
