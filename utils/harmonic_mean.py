"""Harmonic mean helpers for rates and parallel quantities."""
import logging

LOG = logging.getLogger(__name__)


def harmonic_mean(values):
    """Return the harmonic mean, guarding against empty or non-positive input."""
    items = [float(v) for v in values or []]
    if not items:
        return 0.0
    if any(v <= 0 for v in items):
        raise ValueError('harmonic mean requires strictly positive values')
    return len(items) / sum(1.0 / v for v in items)


def combined_rate(rates):
    """Return the effective combined rate of several sequential estimates."""
    return harmonic_mean(rates)


def parallel_equivalent(components):
    """Return the equivalent of components arranged in parallel."""
    items = [float(v) for v in components or []]
    if not items:
        return 0.0
    if any(v <= 0 for v in items):
        raise ValueError('components must be strictly positive')
    return 1.0 / sum(1.0 / v for v in items)


__all__ = ['harmonic_mean', 'combined_rate', 'parallel_equivalent']
