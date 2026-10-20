"""Round timestamps down to a fixed size bucket.

Buckets keep counter series aligned across hosts so they can be summed without
resampling, and are the cheapest way to coarsen a time axis.
"""
import logging

LOG = logging.getLogger(__name__)


def floor_to_bucket(timestamp, bucket_seconds):
    """Round a timestamp down to the start of its bucket."""
    size = int(bucket_seconds)
    if size <= 0:
        raise ValueError("bucket_seconds must be positive")
    return (int(timestamp) // size) * size


def ceil_to_bucket(timestamp, bucket_seconds):
    """Round a timestamp up to the end of its bucket."""
    size = int(bucket_seconds)
    if size <= 0:
        raise ValueError("bucket_seconds must be positive")
    return floor_to_bucket(timestamp, size) + size


def bucket_index(timestamp, bucket_seconds):
    """Return the integer index of the bucket containing the timestamp."""
    return floor_to_bucket(timestamp, bucket_seconds) // int(bucket_seconds)


__all__ = ["floor_to_bucket", "ceil_to_bucket", "bucket_index"]
