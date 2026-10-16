"""Exponential backoff schedule with jitter.

Retrying a failed agent call without any pause amplifies an outage, whereas a
capped exponential schedule spreads retries and respects remote rate limits.
"""
import random
import logging

LOG = logging.getLogger(__name__)


def backoff_delay(attempt, base=1.0, cap=60.0):
    """Return the exponential delay for a zero based attempt number."""
    if attempt < 0:
        raise ValueError('attempt must not be negative')
    delay = min(cap, base * (2 ** attempt))
    LOG.debug('attempt %d backoff %.2fs', attempt, delay)
    return delay


def jittered_delay(attempt, base=1.0, cap=60.0, jitter=0.3, rng=None):
    """Return a backoff delay randomised by the given jitter fraction."""
    delay = backoff_delay(attempt, base, cap)
    source = rng if rng is not None else random
    spread = delay * jitter
    return round(max(0.0, delay + source.uniform(-spread, spread)), 4)


def delay_series(attempts, base=1.0, cap=60.0):
    """Return plain backoff delays for a run of consecutive attempts."""
    return [backoff_delay(index, base, cap) for index in range(attempts)]


__all__ = ['backoff_delay', 'jittered_delay', 'delay_series']
