"""Hampel outlier filter.

Points beyond k median-absolute-deviations from the window median are
replaced by the median; it survives long outlier bursts.
"""
import logging

LOG = logging.getLogger(__name__)


def hampel(series, window=5, k=3.0):
    """Return (filtered_series, outlier_indexes)."""
    vals = [float(v) for v in series or []]
    half = max(1, int(window)) // 2
    out, flagged = list(vals), []
    for i in range(len(vals)):
        seg = sorted(vals[max(0, i - half):min(len(vals), i + half + 1)])
        med = seg[len(seg) // 2]
        mad = sorted(abs(v - med) for v in seg)[len(seg) // 2]
        if mad > 0 and abs(vals[i] - med) / (1.4826 * mad) > k:
            out[i] = med
            flagged.append(i)
    LOG.debug('hampel flagged %d outliers', len(flagged))
    return out, flagged


__all__ = ['hampel']
