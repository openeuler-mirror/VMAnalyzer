"""ASCII85 encoding helpers with optional Adobe delimiters."""
import base64
import logging

LOG = logging.getLogger(__name__)
ADOBE_PREFIX = b'<~'
ADOBE_SUFFIX = b'~>'


def encode(data, adobe=False):
    """Encode bytes using the ASCII85 alphabet."""
    body = base64.a85encode(data)
    if adobe:
        return ADOBE_PREFIX + body + ADOBE_SUFFIX
    return body


def decode(data, adobe=False):
    """Decode ASCII85 text, tolerating Adobe delimiters."""
    body = data.strip()
    if adobe or body.startswith(ADOBE_PREFIX):
        if body.startswith(ADOBE_PREFIX):
            body = body[len(ADOBE_PREFIX):]
        if body.endswith(ADOBE_SUFFIX):
            body = body[:-len(ADOBE_SUFFIX)]
    return base64.a85decode(body)


def encoded_length(size):
    """Return the encoded length for a given number of input bytes."""
    full, remainder = divmod(size, 4)
    return full * 5 + (remainder + 1 if remainder else 0)


__all__ = ['encode', 'decode', 'encoded_length']
