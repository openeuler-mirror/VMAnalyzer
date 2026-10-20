"""Jaeger trace depth analysis.

Deeply nested spans hint at chatty service calls; measuring the maximum
depth of the span tree keeps call graphs shallow.
"""
import logging

LOG = logging.getLogger(__name__)


def max_depth(spans):
    """Return the longest parent chain among spans."""
    parent_of = {s.get('span_id'): s.get('parent_id') for s in spans or []}
    best = 0
    for sid in parent_of:
        depth, cur, seen = 0, sid, set()
        while cur in parent_of and cur not in seen:
            seen.add(cur)
            depth += 1
            cur = parent_of.get(cur)
        best = max(best, depth)
    LOG.debug('trace max depth %d', best)
    return best


def root_spans(spans):
    """Return spans without a parent in the same trace."""
    ids = {s.get('span_id') for s in spans or []}
    return [s for s in spans or [] if s.get('parent_id') not in ids]


__all__ = ['max_depth', 'root_spans']
