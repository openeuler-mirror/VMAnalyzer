"""Compute retention cutoffs and expiry decisions for time series data."""

_UNITS = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}


def parse_retention(text):
    """Parse a retention string such as ``30d`` into seconds, or ``None``."""
    token = (text or "").strip().lower()
    if not token:
        return None
    unit = token[-1]
    if unit not in _UNITS:
        return None
    try:
        amount = float(token[:-1])
    except ValueError:
        return None
    return int(amount * _UNITS[unit])


def cutoff_timestamp(now, retention_seconds):
    """Return the oldest timestamp that should still be retained."""
    return now - retention_seconds


def is_expired(timestamp, now, retention_seconds):
    """Return True when a sample is older than the retention window."""
    return timestamp < cutoff_timestamp(now, retention_seconds)


def retention_summary(now, tiers):
    """Return ``(tier_name, cutoff)`` pairs evaluated from a tier mapping."""
    return [(name, cutoff_timestamp(now, seconds))
            for name, seconds in sorted(tiers.items(), key=lambda kv: kv[1])]


__all__ = ["parse_retention", "cutoff_timestamp", "is_expired", "retention_summary"]
