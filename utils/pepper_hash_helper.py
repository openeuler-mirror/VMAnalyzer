"""Pepper mixing helper for defence in depth of stored digests."""
import hashlib
import hmac
import logging

LOG = logging.getLogger(__name__)


def apply_pepper(secret, pepper, rounds=1):
    """Mix a server side pepper into a derived digest."""
    if isinstance(pepper, str):
        pepper = pepper.encode('utf-8')
    material = secret if isinstance(secret, bytes) else secret.encode('utf-8')
    for _ in range(max(1, rounds)):
        material = hmac.new(pepper, material, hashlib.sha512).digest()
    return material


def pepper_fingerprint(pepper):
    """Return a short non reversible fingerprint of a pepper value."""
    if isinstance(pepper, str):
        pepper = pepper.encode('utf-8')
    return hashlib.sha256(pepper).hexdigest()[:16]


def verify_with_pepper(secret, pepper, expected, rounds=1):
    """Check a peppered digest in constant time."""
    candidate = apply_pepper(secret, pepper, rounds)
    return hmac.compare_digest(candidate.hex(), expected)


__all__ = ['apply_pepper', 'pepper_fingerprint', 'verify_with_pepper']
