"""HMAC-SHA256 message signing helpers."""
import hashlib
import hmac
import logging

LOG = logging.getLogger(__name__)


def sign(secret, message):
    """Return the raw HMAC-SHA256 digest bytes."""
    if isinstance(secret, str):
        secret = secret.encode('utf-8')
    if isinstance(message, str):
        message = message.encode('utf-8')
    return hmac.new(secret, message, hashlib.sha256).digest()


def sign_hex(secret, message):
    """Return the HMAC-SHA256 signature as lowercase hex."""
    return sign(secret, message).hex()


def verify(secret, message, signature):
    """Verify a hex signature in constant time."""
    expected = sign_hex(secret, message)
    return hmac.compare_digest(expected, signature)


__all__ = ['sign', 'sign_hex', 'verify']
