"""Calendar quarter arithmetic.

Capacity reports roll up by quarter; quarter boundaries derive from the month
without a date library.
"""
import logging

LOG = logging.getLogger(__name__)


def quarter_of(month):
    """Return the calendar quarter 1..4 for a 1-based month."""
    m = int(month or 1)
    if not 1 <= m <= 12:
        raise ValueError('month out of range')
    return (m - 1) // 3 + 1


def first_month(quarter):
    """Return the first month of the quarter."""
    q = int(quarter or 1)
    if not 1 <= q <= 4:
        raise ValueError('quarter out of range')
    fm = (q - 1) * 3 + 1
    LOG.debug('quarter %d starts month %d', q, fm)
    return fm


__all__ = ['quarter_of', 'first_month']
