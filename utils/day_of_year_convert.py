"""Day of year conversion helpers.

Translates between a date and its 1-based day of year and back, which is handy
for seasonal baselines keyed on position in the year.
"""
import datetime as _dt


def day_of_year(day):
    """Return the 1-based day of year for a date."""
    return day.timetuple().tm_yday


def is_leap_year(year):
    """Report whether a year has 366 days."""
    return _dt.date(year, 12, 31).timetuple().tm_yday == 366


def from_day_of_year(year, ordinal):
    """Return the date for a 1-based day of year within a year."""
    base = _dt.date(year, 1, 1)
    return base + _dt.timedelta(days=int(ordinal) - 1)


__all__ = ["day_of_year", "is_leap_year", "from_day_of_year"]
