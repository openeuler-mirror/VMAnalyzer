"""Linear interpolation and extrapolation over sample pairs."""
import logging

LOG = logging.getLogger(__name__)


def interpolate(x, x0, y0, x1, y1):
    """Return the linear interpolation of y at x between two known points."""
    if x1 == x0:
        raise ValueError('x0 and x1 must differ')
    slope = (y1 - y0) / float(x1 - x0)
    return y0 + slope * (x - x0)


def interpolate_series(xs, ys, x):
    """Interpolate y at x inside a monotone series, clamping outside it."""
    pairs = sorted(zip(xs or [], ys or []))
    if not pairs:
        return 0.0
    if x <= pairs[0][0]:
        return float(pairs[0][1])
    if x >= pairs[-1][0]:
        return float(pairs[-1][1])
    for left, right in zip(pairs, pairs[1:]):
        if left[0] <= x <= right[0]:
            return interpolate(x, left[0], left[1], right[0], right[1])
    return float(pairs[-1][1])


def lerp(start, end, fraction):
    """Return the point a given fraction of the way from start to end."""
    return start + (end - start) * fraction


__all__ = ['interpolate', 'interpolate_series', 'lerp']
