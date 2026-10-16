"""Deterministic idempotency key derivation for retried actions.

Replaying an action after a network timeout must not duplicate its effect, so
the key is derived from the operation and its arguments only, never from time.
"""
import hashlib
import logging

LOG = logging.getLogger(__name__)


def canonical_args(*args, **kwargs):
    """Render arguments into a stable, sorted canonical string."""
    parts = [repr(arg) for arg in args]
    for key in sorted(kwargs):
        parts.append('%s=%r' % (key, kwargs[key]))
    return '|'.join(parts)


def idempotency_key(operation, *args, **kwargs):
    """Return a stable hex digest for an operation and its arguments."""
    payload = '::'.join([str(operation), canonical_args(*args, **kwargs)])
    digest = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    LOG.debug('idempotency key for %s derived', operation)
    return digest[:32]


def is_replay(key, seen):
    """Report whether the key was already recorded, and record it otherwise."""
    if key in seen:
        return True
    seen.add(key)
    return False


__all__ = ['canonical_args', 'idempotency_key', 'is_replay']
