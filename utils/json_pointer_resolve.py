"""Resolve RFC 6901 JSON pointers against parsed documents."""
import logging

LOG = logging.getLogger(__name__)


def parse_pointer(pointer):
    """Split a JSON pointer into its unescaped reference tokens."""
    if pointer == '':
        return []
    if not pointer.startswith('/'):
        raise ValueError('pointer must be empty or start with a slash')
    tokens = []
    for token in pointer.split('/')[1:]:
        tokens.append(token.replace('~1', '/').replace('~0', '~'))
    return tokens


def resolve(document, pointer, default=None):
    """Walk a document following a pointer, returning default on a miss."""
    node = document
    try:
        for token in parse_pointer(pointer):
            node = node[int(token)] if isinstance(node, list) else node[token]
    except (KeyError, IndexError, ValueError, TypeError):
        return default
    return node


def exists(document, pointer):
    """Report whether a pointer resolves inside a document."""
    marker = object()
    return resolve(document, pointer, marker) is not marker


__all__ = ['parse_pointer', 'resolve', 'exists']
