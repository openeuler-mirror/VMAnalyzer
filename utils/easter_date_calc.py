"""Anonymous Gregorian Easter algorithm.

Computes the Gregorian Easter Sunday date without external tables, which is the
anchor for many movable feasts.
"""
import datetime as _dt


def easter_date(year):
    """Return the Gregorian Easter Sunday date for a year."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    m = (32 + 2 * e + 2 * i - h - k) % 7
    n = (a + 11 * h + 22 * m) // 451
    month = (h + m - 7 * n + 114) // 31
    day = ((h + m - 7 * n + 114) % 31) + 1
    return _dt.date(year, month, day)


def is_easter(day):
    """Report whether a date is Easter Sunday."""
    return day == easter_date(day.year)


__all__ = ["easter_date", "is_easter"]
