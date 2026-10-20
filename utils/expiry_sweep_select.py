"""Select expired records for a sweep cycle.

Bounds how many records a sweep removes per cycle so a large expiry wave does
not overwhelm downstream systems.
"""
import logging

LOG = logging.getLogger(__name__)


def expired(records, now):
    """Return records whose expiry time has passed."""
    return [record for record in records if record.get("expires_at", now + 1) <= now]


def select_batch(records, now, batch_size):
    """Return the oldest expired records up to the batch size."""
    candidates = expired(records, now)
    candidates.sort(key=lambda record: record.get("expires_at", 0))
    return candidates[:max(0, batch_size)]


def sweep_backlog(records, now):
    """Return how many expired records still await a sweep."""
    return len(expired(records, now))


__all__ = ["expired", "select_batch", "sweep_backlog"]
