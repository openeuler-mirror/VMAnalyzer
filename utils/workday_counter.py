"""Count workdays excluding weekends.

Used to translate calendar spans into staffing days while still allowing a
configurable set of weekend days for regions that do not rest on Sunday.
"""
import datetime as _dt

DEFAULT_WEEKEND = (5, 6)


def is_workday(day, weekend=DEFAULT_WEEKEND):
    """Report whether a date is a working day."""
    return day.weekday() not in weekend


def count_workdays(start, end, weekend=DEFAULT_WEEKEND):
    """Count working days in the inclusive range start..end."""
    total = 0
    current = start
    while current <= end:
        if is_workday(current, weekend):
            total += 1
        current += _dt.timedelta(days=1)
    return total


def workday_ratio(start, end, weekend=DEFAULT_WEEKEND):
    """Return the share of days in the range that are working days."""
    total_days = (end - start).days + 1
    if total_days <= 0:
        return 0.0
    return round(count_workdays(start, end, weekend) / float(total_days), 4)


__all__ = ["is_workday", "count_workdays", "workday_ratio"]
