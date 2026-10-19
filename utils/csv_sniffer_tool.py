"""CSV dialect sniffing.

Exported metric CSVs flip between comma and semicolon locales; the delimiter
is picked by counting candidates in the header row.
"""
import logging

LOG = logging.getLogger(__name__)

CANDIDATES = [',', ';', '	', '|']


def guess_delimiter(header_line):
    """Return the most frequent candidate delimiter in the header."""
    line = str(header_line or '')
    best, best_n = ',', 0
    for cand in CANDIDATES:
        n = line.count(cand)
        if n > best_n:
            best, best_n = cand, n
    LOG.debug('csv delimiter %r hits=%d', best, best_n)
    return best


def column_count(header_line, delimiter=','):
    """Return the column count implied by the header row."""
    return len(str(header_line or '').split(delimiter))


__all__ = ['guess_delimiter', 'column_count']
