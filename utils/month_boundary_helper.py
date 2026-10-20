"""Month boundary helpers.

Computes the first and last instant of a month and answers whether a date sits
on a boundary, which drives monthly billing and rollup jobs.
"""
import calendar


def first_day(day):
    """Return the first calendar day of the given month."""
    return day.replace(day=1)


def last_day(day):
    """Return the last calendar day of the given month."""
    days = calendar.monthrange(day.year, day.month)[1]
    return day.replace(day=days)


def is_month_start(day):
    """Report whether the date is the first day of its month."""
    return day.day == 1


__all__ = ["first_day", "last_day", "is_month_start"]
