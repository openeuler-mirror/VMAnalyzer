"""Compose stable deduplication keys for scheduled jobs.

A job key combines the job name with its scheduled slot so a retried scheduler
run does not enqueue the same work twice.
"""
import hashlib
import logging

LOG = logging.getLogger(__name__)


def slot_key(name, slot, bucket_seconds=60):
    """Return a stable key for a job name and aligned time slot."""
    aligned = (int(slot) // int(bucket_seconds)) * int(bucket_seconds)
    return "%s@%d" % (name, aligned)


def hashed_key(name, slot, bucket_seconds=60):
    """Return a short hexadecimal digest of the slot key."""
    raw = slot_key(name, slot, bucket_seconds).encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:16]


def is_duplicate(seen, name, slot, bucket_seconds=60):
    """Report whether the key for this job slot was already seen."""
    return slot_key(name, slot, bucket_seconds) in seen


__all__ = ["slot_key", "hashed_key", "is_duplicate"]
