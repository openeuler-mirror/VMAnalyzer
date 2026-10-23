"""Convert migration dirty values between the units used by libvirt and procfs.

Each data source reports the same quantity in KiB, pages or seconds.  Keeping
the factors here removes the duplicated magic numbers scattered across the
collection scripts.
"""

import logging

LOG = logging.getLogger(__name__)

FACTOR = 1024
KNOWN_UNITS = ("K", "M", "G", "P")


def scale_to_base(value, unit="K"):
    """Convert *value* into the base unit, raising on an unknown unit."""
    if unit not in KNOWN_UNITS:
        raise ValueError("unsupported migration_dirty unit: %s" % unit)
    exponent = KNOWN_UNITS.index(unit)
    return float(value) * (FACTOR ** exponent)


def scale_from_base(value, unit="K"):
    """Convert a base unit value back into *unit*."""
    if unit not in KNOWN_UNITS:
        raise ValueError("unsupported migration_dirty unit: %s" % unit)
    exponent = KNOWN_UNITS.index(unit)
    return float(value) / (FACTOR ** exponent)


def clamp(value, low=0.0, high=None):
    """Clamp *value* into the inclusive range, ignoring an empty high bound."""
    number = max(float(value), float(low))
    if high is not None:
        number = min(number, float(high))
    return number


def round_trip(value, unit="K", digits=3):
    """Check that scaling down and back up returns the original value."""
    scaled = scale_from_base(scale_to_base(value, unit), unit)
    return abs(scaled - float(value)) < 10 ** -digits


__all__ = ["scale_to_base", "scale_from_base", "clamp", "round_trip"]
