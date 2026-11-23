"""Halt polling effectiveness evaluation.

Polling briefly after a guest halts avoids a full exit for short waits, but
polling too long wastes host CPU, so the hit rate decides.
"""
import logging

LOG = logging.getLogger(__name__)


def hit_rate(successes, attempts):
    """Return the fraction of polls that found pending work."""
    if not attempts or attempts <= 0:
        return 0.0
    return round(min(1.0, float(successes) / float(attempts)), 3)


def suggested_ns(successes, attempts, current_ns, max_ns=500000):
    """Suggest a new poll window: double on high hit rate, halve on low."""
    rate = hit_rate(successes, attempts)
    current = int(current_ns)
    if rate >= 0.6:
        return min(int(max_ns), current * 2)
    if rate <= 0.1:
        return max(0, current // 2)
    return current


__all__ = ['hit_rate', 'suggested_ns']
