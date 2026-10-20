"""Gap buffer move cost.

Editors move the gap to the cursor; the copy cost of a move is the distance
times average line size.
"""
import logging

LOG = logging.getLogger(__name__)


def move_cost(gap_pos, cursor_pos, avg_line_bytes=64):
    """Return bytes copied to move the gap to the cursor."""
    cost = abs(int(cursor_pos or 0) - int(gap_pos or 0)) * int(avg_line_bytes or 1)
    LOG.debug('gap move copies %d bytes', cost)
    return cost


def grow_size(current_size):
    """Return the doubled buffer size with a minimum floor."""
    return max(64, int(current_size or 0) * 2)


__all__ = ['move_cost', 'grow_size']
