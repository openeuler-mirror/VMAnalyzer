"""Garbage collection pause analysis.

Throughput is rarely harmed by garbage volume itself but by long stop the world
pauses, so the pause duration distribution is analysed rather than collection
counts.
"""
import statistics
import logging

LOG = logging.getLogger(__name__)


def pause_summary(pauses_ms):
    """Return count, total, worst and mean pause duration."""
    values = sorted(float(p) for p in pauses_ms or [] if p is not None)
    if not values:
        LOG.debug('no pause samples available')
        return {'count': 0}
    return {
        'count': len(values),
        'total_ms': round(sum(values), 3),
        'worst_ms': round(values[-1], 3),
        'mean_ms': round(statistics.fmean(values), 3),
    }


def pause_ratio(pauses_ms, window_seconds):
    """Return the share of the window spent paused."""
    if window_seconds <= 0:
        return 0.0
    total = sum(float(p) for p in pauses_ms or [] if p is not None)
    return round(min(1.0, total / (float(window_seconds) * 1000.0)), 4)


def pause_verdict(summary, worst_limit_ms=500.0):
    """Classify pause durations as healthy, degraded or severe."""
    if summary.get('count', 0) == 0:
        return 'unknown'
    if summary['worst_ms'] >= worst_limit_ms:
        return 'severe'
    if summary['mean_ms'] >= worst_limit_ms / 10.0:
        return 'degraded'
    return 'healthy'


__all__ = ['pause_summary', 'pause_ratio', 'pause_verdict']
