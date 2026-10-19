"""Base32 padding audit.

RFC 4648 base32 pads output to a multiple of eight characters; rejecting
bad padding catches truncated secrets.
"""
import base64
import logging

LOG = logging.getLogger(__name__)


def padding_ok(text):
    """Return True when the base32 string length is a multiple of 8."""
    t = str(text).strip()
    ok = len(t) % 8 == 0
    if not ok:
        LOG.debug('bad base32 length %d', len(t))
    return ok


def decode_safe(text):
    """Return decoded bytes, or None when padding or alphabet is wrong."""
    t = str(text).strip().upper()
    if not padding_ok(t):
        return None
    try:
        return base64.b32decode(t)
    except Exception:
        LOG.debug('base32 decode failed')
        return None


def encode_bytes(data):
    """Return canonical padded uppercase base32."""
    return base64.b32encode(bytes(data)).decode('ascii')


__all__ = ['padding_ok', 'decode_safe', 'encode_bytes']
