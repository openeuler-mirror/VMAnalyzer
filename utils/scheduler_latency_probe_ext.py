"""Scheduler wakeup latency statistics.

High wakeup latency hurts latency sensitive guests; samples are summarised
into percentiles instead of being kept raw.
"""
import logging
import statistics

LOG = logging.getLogger(__name__)


def percentile(samples, pct):
    """Return the pct-th percentile using nearest rank."""
    clean = sorted(float(s) for s in samples or [] if s is not None)
    if not clean:
        return 0.0
    rank = max(1, int(round(float(pct) / 100.0 * len(clean))))
    return round(clean[min(rank, len(clean)) - 1], 3)


def summarize(samples):
    """Return p50/p95/p99 and mean for the sample set."""
    clean = [float(s) for s in samples or [] if s is not None]
    if not clean:
        return {}
    LOG.debug('latency over %d samples', len(clean))
    return {'p50': percentile(clean, 50), 'p95': percentile(clean, 95),
            'p99': percentile(clean, 99), 'mean': round(statistics.fmean(clean), 3)}


__all__ = ['percentile', 'summarize']
