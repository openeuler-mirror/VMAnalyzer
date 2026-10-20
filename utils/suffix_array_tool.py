"""Suffix array memory estimate.

Full-text search over logs uses a suffix array; its memory is one pointer per
byte of text plus the text itself.
"""
import logging

LOG = logging.getLogger(__name__)


def memory_bytes(text_bytes, pointer_size=8):
    """Return suffix array memory for the corpus size."""
    total = int(text_bytes or 0) * (1 + int(pointer_size or 8))
    LOG.debug('suffix array needs %d bytes', total)
    return total


def fits(text_bytes, budget_bytes, pointer_size=8):
    """Report whether the suffix array fits the memory budget."""
    return memory_bytes(text_bytes, pointer_size) <= int(budget_bytes or 0)


__all__ = ['memory_bytes', 'fits']
