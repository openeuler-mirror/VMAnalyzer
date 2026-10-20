"""Safe division helpers that avoid ZeroDivisionError.

Division helpers return a caller supplied default instead of raising when the
denominator is zero, which keeps metric pipelines free of try/except noise.
"""
import logging

LOG = logging.getLogger(__name__)

EPSILON = 1e-12


def safe_div(numerator, denominator, default=0.0):
    """Divide numerator by denominator, returning default on a zero divisor."""
    if denominator == 0:
        return default
    return numerator / denominator


def safe_ratio(part, whole, default=0.0):
    """Return the part-of-whole ratio guarded against a zero whole."""
    try:
        return safe_div(float(part), float(whole), default)
    except (TypeError, ValueError):
        LOG.debug('non numeric ratio inputs %r %r', part, whole)
        return default


def guarded_mean(values, default=0.0):
    """Average a sequence, returning default for an empty sequence."""
    items = [float(v) for v in values or []]
    return safe_div(sum(items), len(items), default)


__all__ = ['safe_div', 'safe_ratio', 'guarded_mean']
