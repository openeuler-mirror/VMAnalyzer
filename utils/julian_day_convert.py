"""Julian day number conversion.

Converts between calendar dates and the Julian day number, a continuous day
count that is convenient for astronomical and long-span arithmetic.
"""
import datetime as _dt

JD_EPOCH_ORDINAL = 1721425


def to_julian_day(day):
    """Return the Julian day number for a date."""
    return day.toordinal() + JD_EPOCH_ORDINAL


def from_julian_day(number):
    """Return the calendar date for a Julian day number."""
    return _dt.date.fromordinal(int(number) - JD_EPOCH_ORDINAL)


def days_apart(first, second):
    """Return the difference in Julian days between two dates."""
    return to_julian_day(second) - to_julian_day(first)


__all__ = ["to_julian_day", "from_julian_day", "days_apart"]
