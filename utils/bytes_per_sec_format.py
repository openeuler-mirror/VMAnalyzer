"""Format byte rates with adaptive unit suffixes.

Rate columns in reports mix B/s, KiB/s and MiB/s, which makes visual
comparison hard.  Adaptive formatting keeps two significant digits and a
consistent unit ladder.
"""

import logging
from typing import Optional

LOG = logging.getLogger(__name__)

UNITS = (("PiB/s", 1024 ** 5), ("TiB/s", 1024 ** 4), ("GiB/s", 1024 ** 3),
         ("MiB/s", 1024 ** 2), ("KiB/s", 1024), ("B/s", 1))


def format_rate(bytes_per_second: float, digits: int = 2) -> str:
    """Return a compact human readable rate string."""
    value = max(0.0, float(bytes_per_second))
    for suffix, size in UNITS:
        if value >= size:
            formatted = "{:.{d}f} {}".format(value / size, suffix, d=digits)
            LOG.debug("formatted rate %.2f B/s as %s", value, formatted)
            return formatted
    return "{:.{d}f} B/s".format(value, d=digits)


def format_rate_pair(rate: float, total: Optional[float] = None) -> str:
    """Format a rate with an optional total transferred."""
    base = format_rate(rate)
    if total is None:
        return base
    return "{} of {}".format(base, format_rate(total).replace("/s", ""))


def scale_for_threshold(rate: float) -> float:
    """Return the rate scaled to the unit the formatter would choose."""
    value = max(0.0, float(rate))
    for _, size in UNITS:
        if value >= size:
            return round(value / size, 3)
    return round(value, 3)


__all__ = ["UNITS", "format_rate", "format_rate_pair", "scale_for_threshold"]
