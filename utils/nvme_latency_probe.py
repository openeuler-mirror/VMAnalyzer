"""NVMe command latency watchdog.

Kernel reported average latency hides tail spikes, so per-window maxima are
tracked against a millisecond budget.
"""
import logging

LOG = logging.getLogger(__name__)


def over_budget(samples_us, budget_us=10000):
    """Return the share of samples above the latency budget."""
    vals = [float(s) for s in samples_us or [] if s is not None]
    if not vals or budget_us <= 0:
        return 0.0
    over = sum(1 for s in vals if s > budget_us)
    return round(over / float(len(vals)), 3)


def p99_us(samples_us):
    """Return an approximate p99 latency in microseconds."""
    vals = sorted(float(s) for s in samples_us or [] if s is not None)
    if not vals:
        return 0.0
    idx = min(len(vals) - 1, int(0.99 * len(vals)))
    LOG.debug('nvme p99 %.0fus', vals[idx])
    return vals[idx]


__all__ = ['over_budget', 'p99_us']
