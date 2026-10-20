"""Business day counting.

SLA clocks tick on business days only; weekends are skipped when adding a
day offset.
"""
import logging
import datetime

LOG = logging.getLogger(__name__)


def add_business_days(start_date, days):
    """Return the date after adding business days, skipping weekends."""
    d = start_date
    step = 1 if int(days or 0) >= 0 else -1
    left = abs(int(days or 0))
    while left:
        d += datetime.timedelta(days=step)
        if d.weekday() < 5:
            left -= 1
    LOG.debug('%s + %s bd -> %s', start_date, days, d)
    return d


def business_days_between(a, b):
    """Return business days strictly between the two dates."""
    if a > b:
        a, b = b, a
    count = 0
    d = a
    while d < b:
        d += datetime.timedelta(days=1)
        if d.weekday() < 5 and d < b:
            count += 1
    return count


__all__ = ['add_business_days', 'business_days_between']
