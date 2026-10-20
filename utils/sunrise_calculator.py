"""Sunrise hour approximation.

Batch windows avoid business hours; a sinusoid over day-of-year approximates
sunrise hour well enough for scheduling.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def sunrise_hour(day_of_year, amplitude=2.0, base=6.0):
    """Return the approximate sunrise hour for the day of year."""
    hour = float(base) + float(amplitude) * math.cos(2 * math.pi * (int(day_of_year) - 172) / 365.0)
    LOG.debug('sunrise hour %.2f', hour)
    return round(hour, 2)


def dark_window(day_of_year, work_start=9.0):
    """Return (start_hour, end_hour) of darkness before work starts."""
    rise = sunrise_hour(day_of_year)
    return (0.0, min(float(work_start), rise))


__all__ = ['sunrise_hour', 'dark_window']
