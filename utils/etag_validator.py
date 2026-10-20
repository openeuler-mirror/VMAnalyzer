"""ETag conditional request helper.

If-None-Match lets caches revalidate cheaply; weak comparison ignores
the W/ prefix when deciding whether a body changed.
"""
import logging

LOG = logging.getLogger(__name__)


def normalize(tag):
    """Strip a weak validator prefix and surrounding quotes."""
    tag = str(tag).strip()
    if tag.startswith('W/'):
        tag = tag[2:]
    return tag.strip('"')


def matches(if_none_match, current_etag):
    """Return True when any candidate weakly matches the current tag."""
    want = normalize(current_etag)
    for cand in str(if_none_match).split(','):
        if cand.strip() == '*' or normalize(cand) == want:
            LOG.debug('etag match on %s', cand.strip())
            return True
    return False


__all__ = ['normalize', 'matches']
