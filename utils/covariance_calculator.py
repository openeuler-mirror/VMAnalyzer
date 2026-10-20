"""Covariance helpers for paired numeric samples."""
import logging

LOG = logging.getLogger(__name__)


def covariance(xs, ys, population=True):
    """Return the covariance of two equally sized sample sequences."""
    pairs = [(float(x), float(y)) for x, y in zip(xs or [], ys or [])]
    if len(pairs) < 2:
        return 0.0
    mean_x = sum(x for x, _ in pairs) / len(pairs)
    mean_y = sum(y for _, y in pairs) / len(pairs)
    total = sum((x - mean_x) * (y - mean_y) for x, y in pairs)
    divisor = len(pairs) if population else len(pairs) - 1
    return total / divisor


def covariance_matrix(columns):
    """Return the pairwise covariance matrix for a list of columns."""
    data = [list(col) for col in columns or []]
    return [[covariance(data[i], data[j]) for j in range(len(data))]
            for i in range(len(data))]


def mean_difference(xs, ys):
    """Return the mean signed difference between paired samples."""
    pairs = [(float(x), float(y)) for x, y in zip(xs or [], ys or [])]
    if not pairs:
        return 0.0
    return sum(x - y for x, y in pairs) / len(pairs)


__all__ = ['covariance', 'covariance_matrix', 'mean_difference']
