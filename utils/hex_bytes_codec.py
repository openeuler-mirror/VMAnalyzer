"""Hex string and bytes conversion helpers.

These helpers keep text facing code from carrying raw byte literals and make
the intent of a conversion explicit at the call site.
"""
import binascii
import logging

LOG = logging.getLogger(__name__)


def to_bytes(hex_text):
    """Decode a hex string into bytes, ignoring separators."""
    cleaned = ''.join(hex_text.split()).replace(':', '')
    return binascii.unhexlify(cleaned)


def to_hex(raw, upper=False, sep=''):
    """Encode bytes into a hex string with an optional separator."""
    text = binascii.hexlify(raw).decode('ascii')
    if upper:
        text = text.upper()
    if sep:
        text = sep.join(text[i:i + 2] for i in range(0, len(text), 2))
    return text


def looks_like_hex(text, length=None):
    """Report whether a string is valid hex of an optional byte length."""
    cleaned = ''.join(text.split())
    if len(cleaned) % 2:
        return False
    if length is not None and len(cleaned) != length * 2:
        return False
    try:
        binascii.unhexlify(cleaned)
    except (binascii.Error, ValueError):
        return False
    return True


__all__ = ['to_bytes', 'to_hex', 'looks_like_hex']
