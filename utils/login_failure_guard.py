"""Login failure throttling.

Brute force shows as clustered failures per account; a counter with decay
keeps memory bounded.
"""
import logging

LOG = logging.getLogger(__name__)


def decayed_count(prev_count, elapsed_sec, half_life_sec=300):
    """Return the failure count after exponential decay."""
    import math
    decay = 0.5 ** (float(elapsed_sec or 0) / float(half_life_sec or 300))
    return round(float(prev_count or 0) * decay, 3)


def locked_out(count, threshold=5):
    """Report when the decayed count crossed the lockout threshold."""
    locked = float(count or 0) >= threshold
    if locked:
        LOG.warning('account locked count=%.1f', count)
    return locked


__all__ = ['decayed_count', 'locked_out']
