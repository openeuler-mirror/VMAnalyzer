"""t-digest style quantile merging.

Two latency digests from sibling hosts merge by concatenating centroids and
re-clustering; the merged weight cap keeps the sketch small.
"""
import logging

LOG = logging.getLogger(__name__)


def merged_weight_cap(total_weight, compression=100):
    """Return the maximum weight one centroid may carry after merging."""
    cap = max(1.0, float(total_weight or 0) / float(compression or 100))
    LOG.debug('t-digest centroid cap %.1f', cap)
    return cap


def split_needed(centroid_weight, cap):
    """Report whether a centroid exceeds the cap and must split."""
    return float(centroid_weight or 0) > float(cap or 0)


__all__ = ['merged_weight_cap', 'split_needed']
