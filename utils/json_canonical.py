"""Canonical JSON serialisation with sorted keys."""
import json
import logging

LOG = logging.getLogger(__name__)


def canonicalize(payload, ensure_ascii=True):
    """Serialise an object to canonical JSON with sorted keys."""
    return json.dumps(payload, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=ensure_ascii)


def canonical_bytes(payload):
    """Return canonical JSON encoded as UTF-8 bytes."""
    return canonicalize(payload, ensure_ascii=False).encode('utf-8')


def same_document(left, right):
    """Report whether two objects canonicalise to the same JSON text."""
    return canonicalize(left) == canonicalize(right)


__all__ = ['canonicalize', 'canonical_bytes', 'same_document']
