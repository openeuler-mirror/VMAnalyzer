"""Grapheme cluster counting.

User-perceived characters join code points with combining marks; counting
clusters keeps truncation from splitting emoji.
"""
import logging
import unicodedata

LOG = logging.getLogger(__name__)


def cluster_count(text):
    """Return an approximate grapheme cluster count."""
    count = 0
    for ch in str(text or ''):
        if unicodedata.combining(ch) == 0 and ch != '‍':
            count += 1
    LOG.debug('grapheme clusters %d', count)
    return count


def safe_truncate(text, max_clusters):
    """Return the text cut to at most max_clusters clusters."""
    out = []
    used = 0
    for ch in str(text or ''):
        joins = unicodedata.combining(ch) != 0 or ch == '‍'
        if not joins and used >= int(max_clusters or 0):
            break
        out.append(ch)
        if not joins:
            used += 1
    return ''.join(out)


__all__ = ['cluster_count', 'safe_truncate']
