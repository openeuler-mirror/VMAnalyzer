"""fsync latency percentiles.

Commit latency dominates database write stalls, so fsync samples are reduced
to a p50/p99 pair for dashboards.
"""
import logging

LOG = logging.getLogger(__name__)


def percentile(sorted_vals, q):
    """Return the q-quantile of an already sorted list."""
    vals = [v for v in sorted_vals or [] if v is not None]
    if not vals:
        return 0.0
    idx = min(len(vals) - 1, max(0, int(q * len(vals))))
    return vals[idx]


def summary(samples_ms):
    """Return (p50, p99) in milliseconds for the samples."""
    vals = sorted(float(s) for s in samples_ms or [] if s is not None)
    pair = (percentile(vals, 0.50), percentile(vals, 0.99))
    LOG.debug('fsync p50=%.2fms p99=%.2fms', pair[0], pair[1])
    return pair


__all__ = ['percentile', 'summary']
