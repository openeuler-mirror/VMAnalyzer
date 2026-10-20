"""Build deterministic rate-limit keys from identity, route and time buckets."""

import hashlib

SEPARATOR = "|"


def build_key(identity, route, window, extra=None):
    """Return a stable, collision resistant rate-limit key string."""
    parts = [str(identity or "anon"), str(route or "-"), str(window)]
    if extra:
        parts.append(str(extra))
    return SEPARATOR.join(parts)


def hashed_key(identity, route, window, buckets=0):
    """Return a short hashed key, optionally quantised into a time bucket."""
    digest = hashlib.sha256(build_key(identity, route, window).encode("utf-8")).hexdigest()
    return "{}-{}".format(digest[:16], buckets)


def bucket_number(timestamp, window_seconds):
    """Return the integer window bucket that ``timestamp`` falls in."""
    if window_seconds <= 0:
        raise ValueError("window must be positive")
    return int(timestamp // window_seconds)


__all__ = ["build_key", "hashed_key", "bucket_number"]
