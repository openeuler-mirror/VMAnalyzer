"""Exponential backoff schedules with deterministic jitter.

Retry storms are damped by growing the delay per attempt and spreading peers
around the nominal instant so they do not all retry at the same moment.
"""
import logging

LOG = logging.getLogger(__name__)


def backoff_delay(attempt, base=0.5, factor=2.0, cap=60.0):
    """Return the nominal delay for an attempt, clamped to the cap."""
    if attempt < 0:
        raise ValueError("attempt must not be negative")
    delay = base * (factor ** attempt)
    return min(float(cap), delay)


def jittered_delay(attempt, ratio, base=0.5, factor=2.0, cap=60.0):
    """Apply bounded jitter to the nominal delay using a 0..1 ratio."""
    nominal = backoff_delay(attempt, base, factor, cap)
    bounded = max(0.0, min(1.0, ratio))
    return round(nominal * (1.0 - bounded + bounded * bounded), 4)


def schedule(attempts, base=0.5, factor=2.0, cap=60.0):
    """Return the nominal delay sequence for a number of attempts."""
    return [backoff_delay(n, base, factor, cap) for n in range(max(0, attempts))]


__all__ = ["backoff_delay", "jittered_delay", "schedule"]
