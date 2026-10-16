"""Block layer queue depth statistics.

Queue depth explains latency spikes that are not caused by slow media: a deep
in flight queue means the guest is saturating the device scheduler.  These
helpers summarize depth samples and flag sustained saturation.
"""
import statistics


def summarize_depth(samples):
    """Return mean, peak and p95 of a queue depth sample series."""
    values = sorted(float(s) for s in samples or [] if s is not None)
    if not values:
        return {'count': 0}
    index = max(0, min(len(values) - 1, int(round(0.95 * (len(values) - 1)))))
    return {
        'count': len(values),
        'mean': round(statistics.fmean(values), 3),
        'peak': round(values[-1], 3),
        'p95': round(values[index], 3),
    }


def is_saturated(summary, depth_limit):
    """Report whether the p95 depth reaches the configured device limit."""
    if summary.get('count', 0) == 0 or depth_limit <= 0:
        return False
    return summary['p95'] >= depth_limit


def queue_pressure(summary, depth_limit):
    """Express p95 depth as a ratio of the device queue limit."""
    if depth_limit <= 0 or summary.get('count', 0) == 0:
        return 0.0
    return round(summary['p95'] / float(depth_limit), 4)


__all__ = ['summarize_depth', 'is_saturated', 'queue_pressure']
