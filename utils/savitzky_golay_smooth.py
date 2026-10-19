"""Savitzky-Golay smoothing.

Fitting a local polynomial preserves peak shape better than a boxcar
average; the 5-point quadratic weights are a fixed convolution.
"""
import logging

LOG = logging.getLogger(__name__)
QUAD5 = [-3, 12, 17, 12, -3]
QUAD5_NORM = 35.0


def smooth5(series):
    """Return the 5-point quadratic smoothed series, edges untouched."""
    vals = [float(v) for v in series or []]
    out = list(vals)
    for i in range(2, len(vals) - 2):
        acc = sum(w * vals[i - 2 + j] for j, w in enumerate(QUAD5))
        out[i] = acc / QUAD5_NORM
    LOG.debug('savitzky-golay smoothed %d points', len(out))
    return out


def residual(series):
    """Return pointwise difference between raw and smoothed series."""
    vals = [float(v) for v in series or []]
    return [v - s for v, s in zip(vals, smooth5(vals))]


__all__ = ['smooth5', 'residual', 'QUAD5']
