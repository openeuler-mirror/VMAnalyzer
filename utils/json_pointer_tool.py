"""JSON Pointer path splitting.

RFC 6901 pointers escape slashes as ~1 and tildes as ~0; splitting without
unescaping corrupts keys that contain tildes.
"""
import logging

LOG = logging.getLogger(__name__)


def split(pointer):
    """Return the unescaped reference tokens of a JSON pointer."""
    raw = str(pointer or '')
    if not raw:
        return []
    if not raw.startswith('/'):
        LOG.warning('pointer lacks leading slash: %r', raw)
        return []
    return [tok.replace('~1', '/').replace('~0', '~') for tok in raw[1:].split('/')]


def escape(token):
    """Return the token with pointer escaping applied."""
    return str(token or '').replace('~', '~0').replace('/', '~1')


__all__ = ['split', 'escape']
