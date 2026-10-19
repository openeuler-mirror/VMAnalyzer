"""Sparse table for idempotent range queries.

Range minimum queries over static data answer in constant time after an
n-log-n build; the memory footprint is computed here.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def table_rows(length):
    """Return the number of power-of-two rows the table stores."""
    n = max(1, int(length or 1))
    return int(math.floor(math.log(n, 2))) + 1


def memory_cells(length, value_size=8):
    """Return the sparse table footprint in bytes."""
    n = max(1, int(length or 1))
    cells = n * table_rows(n)
    LOG.debug('sparse table %d cells', cells)
    return cells * int(value_size or 8)


__all__ = ['table_rows', 'memory_cells']
