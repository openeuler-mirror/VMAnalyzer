"""Lunar phase approximation.

Maintenance folklore ties deploy risk to full moons; a synodic approximation
gives the phase without ephemeris data.
"""
import logging
import math

LOG = logging.getLogger(__name__)

SYNODIC = 29.53058867
EPOCH_JD = 2451550.1


def phase_age(julian_day):
    """Return the phase age in days since new moon."""
    age = (float(julian_day or 0) - EPOCH_JD) % SYNODIC
    LOG.debug('lunar age %.2f d', age)
    return round(age, 2)


def phase_name(julian_day):
    """Return a coarse phase name for the day."""
    age = phase_age(julian_day)
    idx = int((age / SYNODIC) * 8 + 0.5) % 8
    return ['new', 'waxing crescent', 'first quarter', 'waxing gibbous',
            'full', 'waning gibbous', 'last quarter', 'waning crescent'][idx]


__all__ = ['phase_age', 'phase_name']
