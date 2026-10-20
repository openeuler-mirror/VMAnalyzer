"""ISO week numbering.

Weekly metrics align to ISO weeks whose year can differ from the calendar
year at the edges; the ordinal math is kept here.
"""
import logging
import datetime

LOG = logging.getLogger(__name__)


def iso_year_week(year, month, day):
    """Return (iso_year, iso_week) for the calendar date."""
    d = datetime.date(int(year), int(month), int(day))
    iso = d.isocalendar()
    LOG.debug('%s -> ISO %d-W%02d', d, iso[0], iso[1])
    return iso[0], iso[1]


def weeks_in_year(year):
    """Return 52 or 53 ISO weeks for the year."""
    return datetime.date(int(year), 12, 28).isocalendar()[1]


__all__ = ['iso_year_week', 'weeks_in_year']
