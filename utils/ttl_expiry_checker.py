"""Time to live expiry decisions.

A tiny value object plus helpers answer whether a cached entry has outlived its
configured lifetime given an explicit observation time.
"""
from dataclasses import dataclass


@dataclass
class TtlEntry:
    """An entry with an insertion time and a lifetime in seconds."""

    inserted_at: float
    ttl_seconds: float

    def expires_at(self):
        """Return the absolute expiry timestamp."""
        return self.inserted_at + self.ttl_seconds

    def is_expired(self, now):
        """Report whether the entry has expired at the observation time."""
        return now >= self.expires_at()

    def remaining(self, now):
        """Return the seconds left before expiry, never negative."""
        return max(0.0, self.expires_at() - now)


def expired_entries(entries, now):
    """Filter a mapping of name to entry down to the expired ones."""
    return [name for name, entry in entries.items() if entry.is_expired(now)]


__all__ = ["TtlEntry", "expired_entries"]
