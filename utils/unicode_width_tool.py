"""Unicode display width estimate.

East-Asian wide glyphs take two cells; misestimating width breaks aligned
tables in terminal reports.
"""
import logging
import unicodedata

LOG = logging.getLogger(__name__)


def char_width(ch):
    """Return the terminal cell width of one character."""
    if not ch:
        return 0
    return 2 if unicodedata.east_asian_width(ch) in ('W', 'F') else 1


def text_width(text):
    """Return the summed cell width of the string."""
    w = sum(char_width(c) for c in str(text or ''))
    LOG.debug('text width %d', w)
    return w


__all__ = ['char_width', 'text_width']
