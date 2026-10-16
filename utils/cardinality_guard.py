"""Guard against unbounded label cardinality in emitted metrics.

A label such as a raw request path can explode the series count, so distinct
values are capped and the excess is folded into a catch all bucket.
"""
import logging

LOG = logging.getLogger(__name__)

OVERFLOW = '__other__'


def distinct_count(values):
    """Return the number of distinct values in the series."""
    return len({str(v) for v in values or []})


def cap_labels(values, limit=100):
    """Return a mapping of allowed values to counts, folding the overflow."""
    counts = {}
    for value in values or []:
        counts[str(value)] = counts.get(str(value), 0) + 1
    if len(counts) <= limit:
        return counts
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    kept = dict(ranked[:limit])
    overflow = sum(count for _name, count in ranked[limit:])
    kept[OVERFLOW] = overflow
    LOG.debug('label cardinality capped to %d', limit)
    return kept


def is_over_limit(values, limit=100):
    """Report whether the distinct value count exceeds the limit."""
    return distinct_count(values) > limit


__all__ = ['distinct_count', 'cap_labels', 'is_over_limit']
