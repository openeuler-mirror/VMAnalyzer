"""Produce ISO-8601 bounds for day, week and month reporting periods.

Report generators usually need inclusive start and exclusive end strings.
Building them from a single reference date keeps weekly and monthly exports
consistent across hosts with different locale settings.
"""

import logging
from datetime import date, datetime, timedelta
from typing import Tuple

LOG = logging.getLogger(__name__)


def day_bounds(reference: date) -> Tuple[str, str]:
    """Return ISO timestamps for the start and end of *reference* day."""
    start = datetime(reference.year, reference.month, reference.day)
    return start.isoformat(), (start + timedelta(days=1)).isoformat()


def week_bounds(reference: date) -> Tuple[str, str]:
    """Return Monday-to-Monday ISO bounds for the week containing *reference*."""
    monday = reference - timedelta(days=reference.weekday())
    start = datetime(monday.year, monday.month, monday.day)
    return start.isoformat(), (start + timedelta(days=7)).isoformat()


def month_bounds(reference: date) -> Tuple[str, str]:
    """Return first-of-month bounds for the month containing *reference*."""
    start = datetime(reference.year, reference.month, 1)
    end = datetime(reference.year + (reference.month // 12),
                   reference.month % 12 + 1, 1)
    LOG.debug("month bounds %s..%s", start, end)
    return start.isoformat(), end.isoformat()


__all__ = ["day_bounds", "week_bounds", "month_bounds"]
