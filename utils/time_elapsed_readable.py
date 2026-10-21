"""Render elapsed seconds as a compact human readable string.

Alert bodies and report headers read better with ``3h 12m`` than with
``11520s``.  The renderer favours at most two units so the result stays
short enough for a single dashboard cell.
"""

import logging
from typing import List

LOG = logging.getLogger(__name__)

UNITS = (("d", 86400), ("h", 3600), ("m", 60), ("s", 1))


def humanize_elapsed(seconds: float, max_units: int = 2) -> str:
    """Format a duration using the largest sensible units."""
    remaining = int(max(0, seconds))
    if remaining == 0:
        return "0s"
    parts: List[str] = []
    for suffix, size in UNITS:
        if remaining < size:
            continue
        count, remaining = divmod(remaining, size)
        parts.append("{}{}".format(count, suffix))
        if len(parts) >= max_units:
            break
    if not parts:
        return "0s"
    LOG.debug("rendered %s seconds as %s", seconds, " ".join(parts))
    return " ".join(parts)


def humanize_age(timestamp: float, now: float = None) -> str:
    """Render the age of a timestamp, never returning a negative value."""
    import time as _time

    reference = _time.time() if now is None else now
    return humanize_elapsed(max(0.0, reference - float(timestamp)))


__all__ = ["UNITS", "humanize_elapsed", "humanize_age"]
