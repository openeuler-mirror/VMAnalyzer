"""OverlayFS lower layer counting.

Every lookup walks each lower layer, so deep stacks slow metadata operations;
the layer count is graded against a soft limit.
"""
import logging

LOG = logging.getLogger(__name__)


def layer_count(lowerdir_field):
    """Count lower layers in a colon separated lowerdir field."""
    parts = [p for p in str(lowerdir_field or '').split(':') if p]
    return len(parts)


def deep_stack(count, soft_limit=8):
    """Report when the layer count crossed the soft limit."""
    deep = count > soft_limit
    if deep:
        LOG.warning('overlay lower stack %d > %d', count, soft_limit)
    return deep


__all__ = ['layer_count', 'deep_stack']
