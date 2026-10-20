"""Format the age of a stale observation.

Operators read an age such as 3m ago far faster than an absolute timestamp, so
these helpers render short human labels from a delta in seconds.
"""
import logging

LOG = logging.getLogger(__name__)

_STEPS = (
    ("y", 31536000),
    ("d", 86400),
    ("h", 3600),
    ("m", 60),
)


def age_seconds(observed_at, now):
    """Return a non negative age in seconds."""
    return max(0.0, now - observed_at)


def format_age(observed_at, now):
    """Render a compact label describing how old an observation is."""
    age = age_seconds(observed_at, now)
    if age < 60:
        return "just now"
    for suffix, size in _STEPS:
        if age >= size:
            return "%d%s ago" % (int(age // size), suffix)
    return "just now"


def is_stale(observed_at, now, threshold):
    """Report whether an observation is older than the threshold."""
    return age_seconds(observed_at, now) > threshold


__all__ = ["age_seconds", "format_age", "is_stale"]
