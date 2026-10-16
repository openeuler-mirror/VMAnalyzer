"""Guard for opaque base64 payloads before they are decoded.

Blindly decoding an incoming blob can exhaust memory or yield an unexpected
type, so the alphabet, padding and size are validated first.
"""
import base64
import binascii
import logging

LOG = logging.getLogger(__name__)

ALPHABET = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')


def looks_like_base64(text):
    """Report whether every character belongs to the base64 alphabet."""
    stripped = str(text or '').strip()
    if not stripped:
        return False
    return all(char in ALPHABET for char in stripped)


def within_budget(text, max_bytes=1048576):
    """Report whether the decoded size stays within the byte budget."""
    stripped = str(text or '').strip()
    padding = stripped.count('=')
    decoded_size = (len(stripped) // 4) * 3 - padding
    return 0 <= decoded_size <= max_bytes


def safe_decode(text, max_bytes=1048576):
    """Decode base64 text only when it is well formed and within budget."""
    if not looks_like_base64(text) or not within_budget(text, max_bytes):
        LOG.debug('rejected base64 payload')
        return None
    try:
        return base64.b64decode(str(text).strip(), validate=True)
    except (binascii.Error, ValueError):
        LOG.debug('base64 decode failed')
        return None


__all__ = ['looks_like_base64', 'within_budget', 'safe_decode']
