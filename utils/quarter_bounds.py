"""Calendar quarter boundaries.

Maps a date onto its quarter number and derives that quarter first and last
day, useful for quarterly capacity reviews.
"""
import datetime as _dt


def quarter_number(day):
    """Return the calendar quarter (1..4) for a date."""
    return (day.month - 1) // 3 + 1


def quarter_start(day):
    """Return the first day of the quarter containing the date."""
    month = (quarter_number(day) - 1) * 3 + 1
    return _dt.date(day.year, month, 1)


def quarter_end(day):
    """Return the last day of the quarter containing the date."""
    start = quarter_start(day)
    next_month = start.month + 3
    year = start.year + (1 if next_month > 12 else 0)
    month = next_month - 12 if next_month > 12 else next_month
    return _dt.date(year, month, 1) - _dt.timedelta(days=1)


__all__ = ["quarter_number", "quarter_start", "quarter_end"]
