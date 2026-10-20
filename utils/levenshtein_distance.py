"""Levenshtein row memory.

Full edit-distance matrices are quadratic; two-row dynamic programming bounds
memory to twice the shorter string.
"""
import logging

LOG = logging.getLogger(__name__)


def row_cells(shorter_len):
    """Return cells held by the two-row variant."""
    return 2 * (int(shorter_len or 0) + 1)


def banded_cells(shorter_len, max_distance):
    """Return cells when the band width limits the search."""
    width = 2 * int(max_distance or 0) + 1
    cells = min(row_cells(shorter_len), width * (int(shorter_len or 0) + 1))
    LOG.debug('lev band cells %d', cells)
    return cells


__all__ = ['row_cells', 'banded_cells']
