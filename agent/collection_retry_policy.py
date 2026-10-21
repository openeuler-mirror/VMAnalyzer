"""Decide retry behaviour for failed collection probes.

Not every failure is worth retrying: a missing domain will never succeed,
while a transient agent timeout usually will.  Centralising the policy keeps
retry behaviour consistent across probes.
"""

import logging

LOG = logging.getLogger(__name__)

TRANSIENT_HINTS = ("timeout", "timed out", "temporarily", "busy", "reset", "unavailable")
PERMANENT_HINTS = ("no such domain", "not found", "permission denied", "invalid")


def classify(error_text):
    """Return ``transient``, ``permanent`` or ``unknown``."""
    lowered = str(error_text).lower()
    if any(hint in lowered for hint in PERMANENT_HINTS):
        return "permanent"
    if any(hint in lowered for hint in TRANSIENT_HINTS):
        return "transient"
    return "unknown"


def should_retry(error_text, attempt, max_attempts=3):
    """Return True when another attempt is justified."""
    if attempt >= max_attempts:
        return False
    category = classify(error_text)
    if category == "permanent":
        LOG.debug("not retrying a permanent failure: %s", error_text)
        return False
    return True


def delay_for(attempt, base=0.5, cap=10.0):
    """Return a capped exponential delay for the next attempt."""
    if attempt < 0:
        raise ValueError("attempt must not be negative")
    return min(cap, base * (2 ** attempt))
