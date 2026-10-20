"""Generic webhook HMAC verification.

Senders sign the raw body with a shared secret; comparing hex digests in
constant time defeats replay and forgery.
"""
import hashlib
import hmac
import logging

LOG = logging.getLogger(__name__)


def sign_body(secret, body):
    """Return the hex HMAC-SHA256 of body under secret."""
    mac = hmac.new(str(secret).encode(), body, hashlib.sha256)
    return mac.hexdigest()


def verify_signature(secret, body, header_value):
    """Return True when the header digest matches, in constant time."""
    expected = sign_body(secret, body)
    provided = str(header_value).replace('sha256=', '')
    ok = hmac.compare_digest(expected, provided)
    if not ok:
        LOG.debug('webhook signature mismatch')
    return ok


__all__ = ['sign_body', 'verify_signature']
