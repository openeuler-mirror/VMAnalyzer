"""Quoted printable encoding and decoding helpers."""
import logging
import quopri

LOG = logging.getLogger(__name__)


def encode(data, header=False):
    """Encode bytes as quoted printable text."""
    return quopri.encodestring(data, quotetabs=True, header=header)


def decode(data):
    """Decode quoted printable text back into bytes."""
    try:
        return quopri.decodestring(data)
    except Exception as exc:
        raise ValueError('invalid quoted printable input: {}'.format(exc))


def needs_encoding(data):
    """Report whether a buffer contains bytes that require escaping."""
    return any(byte > 126 or (byte < 32 and byte not in (9, 10, 13)) or byte == 61
               for byte in data)


__all__ = ['encode', 'decode', 'needs_encoding']
