"""Monotonic trend direction classification for a metric series.

Telling an operator that a metric is steadily climbing is more actionable than
a raw delta, so the series is reduced to a small direction label.
"""
import logging

LOG = logging.getLogger(__name__)

RISING = 'rising'
FALLING = 'falling'
FLAT = 'flat'


def monotonic_runs(values):
    """Return the longest rising and falling run lengths in the series."""
    clean = [float(v) for v in values or [] if v is not None]
    up = down = best_up = best_down = 0
    for a, b in zip(clean, clean[1:]):
        if b > a:
            up += 1
            down = 0
        elif b < a:
            down += 1
            up = 0
        else:
            up = down = 0
        best_up = max(best_up, up)
        best_down = max(best_down, down)
    return best_up, best_down


def direction(values, flat_band=1e-9):
    """Classify the series as rising, falling or flat."""
    clean = [float(v) for v in values or [] if v is not None]
    if len(clean) < 2:
        return FLAT
    span = clean[-1] - clean[0]
    if abs(span) <= flat_band:
        return FLAT
    return RISING if span > 0 else FALLING


def confidence(values):
    """Return the share of steps that agree with the overall direction."""
    clean = [float(v) for v in values or [] if v is not None]
    if len(clean) < 2:
        return 0.0
    overall = direction(clean)
    agree = total = 0
    for a, b in zip(clean, clean[1:]):
        if b == a:
            continue
        total += 1
        if (b > a and overall == RISING) or (b < a and overall == FALLING):
            agree += 1
    if total == 0:
        return 0.0
    return round(agree / float(total), 3)


__all__ = ['monotonic_runs', 'direction', 'confidence']
