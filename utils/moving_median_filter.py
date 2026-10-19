"""Moving median filter.

Median windows reject spike noise that a moving average would smear into
the signal, which suits jittery telemetry.
"""
import logging

LOG = logging.getLogger(__name__)


def moving_median(series, window=5):
    """Return the windowed median, None where the window is partial."""
    vals = [float(v) for v in series or []]
    half = max(1, int(window)) // 2
    out = []
    for i in range(len(vals)):
        lo, hi = max(0, i - half), min(len(vals), i + half + 1)
        if hi - lo < window:
            out.append(None)
            continue
        seg = sorted(vals[lo:hi])
        out.append(seg[len(seg) // 2])
    LOG.debug('moving median over %d points', len(out))
    return out


def spike_flags(series, window=5, threshold=3.0):
    """Return indexes whose value deviates from the window median."""
    vals = [float(v) for v in series or []]
    meds = moving_median(vals, window)
    return [i for i, (v, m) in enumerate(zip(vals, meds))
            if m is not None and m != 0 and abs(v - m) / abs(m) > threshold]


__all__ = ['moving_median', 'spike_flags']
