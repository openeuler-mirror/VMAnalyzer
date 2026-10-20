"""Human readable duration rendering.

Turns a number of seconds into a compact label such as 1h 5m, choosing the two
most significant non zero units so dashboards stay readable.
"""
import logging

LOG = logging.getLogger(__name__)

_UNITS = (
    ("d", 86400),
    ("h", 3600),
    ("m", 60),
    ("s", 1),
)


def split_duration(seconds):
    """Return the ordered list of (unit, amount) pairs for a duration."""
    remaining = max(0, int(seconds))
    parts = []
    for unit, size in _UNITS:
        amount, remaining = divmod(remaining, size)
        if amount:
            parts.append((unit, amount))
    return parts


def humanize_duration(seconds, max_units=2):
    """Render a duration using at most max_units leading components."""
    parts = split_duration(seconds)
    if not parts:
        return "0s"
    chosen = parts[:max(1, int(max_units))]
    return " ".join("%d%s" % (amount, unit) for unit, amount in chosen)


__all__ = ["split_duration", "humanize_duration"]
