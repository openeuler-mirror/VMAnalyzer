"""Gini impurity and split quality measures."""
import logging

LOG = logging.getLogger(__name__)


def gini_impurity(counts):
    """Return the Gini impurity of a label count distribution."""
    items = [float(c) for c in counts or []]
    total = sum(items)
    if total <= 0:
        return 0.0
    return 1.0 - sum((c / total) ** 2 for c in items)


def weighted_gini(groups):
    """Return the weighted Gini impurity across several count groups."""
    sizes = [sum(float(c) for c in group or []) for group in groups or []]
    total = sum(sizes)
    if total <= 0:
        return 0.0
    return sum(size / total * gini_impurity(group)
               for size, group in zip(sizes, groups))


def gini_gain(parent, groups):
    """Return the impurity reduction obtained by splitting into groups."""
    return gini_impurity(parent) - weighted_gini(groups)


__all__ = ['gini_impurity', 'weighted_gini', 'gini_gain']
