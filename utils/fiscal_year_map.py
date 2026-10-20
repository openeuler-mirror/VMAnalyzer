"""Map dates onto a configurable fiscal year.

Fiscal calendars rarely start in January, so the mapping accepts an arbitrary
start month and returns both the fiscal year and the month offset within it.
"""
import logging

LOG = logging.getLogger(__name__)


def fiscal_year(day, start_month):
    """Return the fiscal year that contains the date."""
    if not 1 <= start_month <= 12:
        raise ValueError("start_month must be between 1 and 12")
    if day.month >= start_month:
        return day.year
    return day.year - 1


def fiscal_month(day, start_month):
    """Return the 1-based month offset inside the fiscal year."""
    offset = (day.month - start_month) % 12
    return offset + 1


def fiscal_label(day, start_month):
    """Render a fiscal year and month label for reporting."""
    return "FY%d-M%02d" % (fiscal_year(day, start_month), fiscal_month(day, start_month))


__all__ = ["fiscal_year", "fiscal_month", "fiscal_label"]
