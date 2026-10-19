"""Boyer-Moore skip table.

Long needle patterns skip whole windows on mismatch; the bad-character table
size and expected skip are computed here.
"""
import logging

LOG = logging.getLogger(__name__)


def table_entries(alphabet=256):
    """Return the bad-character table size."""
    return int(alphabet or 256)


def expected_skip(needle, text_alphabet=26):
    """Return the average skip distance for a random text."""
    n = len(str(needle or ''))
    if not n:
        return 0.0
    skip = min(n, max(1.0, float(text_alphabet) / max(1, n)))
    LOG.debug('bm expected skip %.2f', skip)
    return round(skip, 2)


__all__ = ['table_entries', 'expected_skip']
