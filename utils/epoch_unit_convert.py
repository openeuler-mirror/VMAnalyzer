"""Epoch seconds and milliseconds conversions.

Monitoring agents disagree on whether they emit seconds or milliseconds since
the epoch, so these helpers normalize both directions with a sanity cutoff.
"""
import logging

LOG = logging.getLogger(__name__)

MS_THRESHOLD = 10 ** 11


def is_milliseconds(value):
    """Guess whether an epoch value is expressed in milliseconds."""
    return abs(int(value)) >= MS_THRESHOLD


def to_seconds(value):
    """Normalize a seconds or milliseconds epoch value into seconds."""
    number = int(value)
    if is_milliseconds(number):
        LOG.debug("dividing epoch value %s by 1000", number)
        return number / 1000.0
    return float(number)


def to_milliseconds(value):
    """Normalize a seconds or milliseconds epoch value into milliseconds."""
    return int(round(to_seconds(value) * 1000))


__all__ = ["is_milliseconds", "to_seconds", "to_milliseconds"]
