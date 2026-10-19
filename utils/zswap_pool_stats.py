"""Zswap pool compression accounting.

The win from zswap is the stored-vs-original byte ratio, plus a reject rate
that rises when the pool is full.
"""
import logging

LOG = logging.getLogger(__name__)


def compression_ratio(stored_bytes, original_bytes):
    """Return stored/original bytes; lower means better compression."""
    if not original_bytes or original_bytes <= 0:
        return 0.0
    return round(float(stored_bytes or 0) / float(original_bytes), 3)


def reject_rate(rejects, attempts):
    """Return pool-full rejects per attempt in 0..1."""
    if not attempts or attempts <= 0:
        return 0.0
    rate = round(min(1.0, float(rejects or 0) / float(attempts)), 4)
    LOG.debug('zswap reject rate %.4f', rate)
    return rate


__all__ = ['compression_ratio', 'reject_rate']
