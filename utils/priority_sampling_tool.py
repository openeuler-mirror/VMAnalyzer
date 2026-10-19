"""Priority sampling for flows.

Keeping the k flows with the smallest random priority yields an unbiased
sample whose weight is the k-th priority.
"""
import logging

LOG = logging.getLogger(__name__)


def horizon(priorities, k):
    """Return the sampling horizon: the k-th smallest priority."""
    vals = sorted(float(p) for p in priorities or [] if p is not None)
    if len(vals) < int(k or 1):
        return 1.0
    h = vals[int(k) - 1]
    LOG.debug('priority horizon %.6f', h)
    return h


def sample_weight(priorities, k):
    """Return the per-item weight implied by the horizon."""
    h = horizon(priorities, k)
    return round(1.0 / h, 3) if h > 0 else 0.0


__all__ = ['horizon', 'sample_weight']
