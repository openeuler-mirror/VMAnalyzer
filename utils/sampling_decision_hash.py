"""Make deterministic sampling decisions by hashing a key into a bucket."""

import hashlib

BUCKETS = 10000


def bucket_of(key, salt=""):
    """Return a stable bucket index for a key in ``[0, BUCKETS)``."""
    digest = hashlib.sha256("{}\x00{}".format(salt, key).encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % BUCKETS


def sample_decision(key, rate, salt=""):
    """Return True when the key should be sampled at ``rate`` in ``[0, 1]``."""
    if rate <= 0:
        return False
    if rate >= 1:
        return True
    return bucket_of(key, salt) < int(rate * BUCKETS)


def sampling_probability(keys, rate, salt=""):
    """Return the observed sampled fraction over an iterable of keys."""
    items = list(keys)
    if not items:
        return 0.0
    chosen = sum(1 for key in items if sample_decision(key, rate, salt))
    return round(chosen / len(items), 4)


__all__ = ["bucket_of", "sample_decision", "sampling_probability"]
