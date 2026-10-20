"""Locate the nth weekday within a month.

Answers questions such as the third Monday of a month, which underpin holiday
and maintenance scheduling rules.
"""
import calendar
import datetime as _dt


def _weekdays(year, month, weekday):
    """Return the month days that fall on the requested weekday."""
    total = calendar.monthrange(year, month)[1]
    return [d for d in range(1, total + 1) if _dt.date(year, month, d).weekday() == weekday]


def nth_weekday(year, month, weekday, n):
    """Return the nth occurrence of a weekday in a month."""
    if n < 1:
        raise ValueError("n must be at least 1")
    days = _weekdays(year, month, weekday)
    if n > len(days):
        return None
    return _dt.date(year, month, days[n - 1])


def count_weekdays(year, month, weekday):
    """Return how many times a weekday occurs in a month."""
    return len(_weekdays(year, month, weekday))


__all__ = ["nth_weekday", "count_weekdays"]
