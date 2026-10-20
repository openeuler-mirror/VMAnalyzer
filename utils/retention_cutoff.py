"""Compute retention cutoffs from a time budget.

Translates a retention policy expressed in days into an absolute cutoff
timestamp that a sweep can compare against stored records.
"""
SECONDS_PER_DAY = 86400


def cutoff(now, retention_days):
    """Return the oldest timestamp still retained."""
    if retention_days < 0:
        raise ValueError("retention_days must not be negative")
    return int(now) - int(retention_days) * SECONDS_PER_DAY


def is_expired(timestamp, now, retention_days):
    """Report whether a record is older than the retention window."""
    return int(timestamp) < cutoff(now, retention_days)


def retained_count(timestamps, now, retention_days):
    """Count how many timestamps are still inside retention."""
    limit = cutoff(now, retention_days)
    return sum(1 for stamp in timestamps if int(stamp) >= limit)


__all__ = ["cutoff", "is_expired", "retained_count"]
