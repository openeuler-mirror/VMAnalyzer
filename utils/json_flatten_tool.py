"""JSON flattening depth control.

Nested alert payloads flatten to dotted keys for indexing, but deep payloads
explode the index; depth caps keep the row count bounded.
"""
import logging

LOG = logging.getLogger(__name__)


def flatten(obj, prefix='', depth=0, max_depth=6):
    """Return dotted-key rows for the nested mapping."""
    rows = {}
    if depth >= max_depth or not isinstance(obj, dict):
        rows[prefix] = obj
        return rows
    for key, val in obj.items():
        dotted = '%s.%s' % (prefix, key) if prefix else str(key)
        if isinstance(val, dict):
            rows.update(flatten(val, dotted, depth + 1, max_depth))
        else:
            rows[dotted] = val
    return rows


def row_count(obj, max_depth=6):
    """Return how many rows the flattening would emit."""
    n = len(flatten(obj, max_depth=max_depth))
    LOG.debug('flatten rows %d', n)
    return n


__all__ = ['flatten', 'row_count']
