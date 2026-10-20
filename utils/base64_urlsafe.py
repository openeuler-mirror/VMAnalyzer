"""URL safe base64 helpers with optional padding control."""
import base64
import logging

LOG = logging.getLogger(__name__)


def encode_urlsafe(raw, padded=True):
    """Encode bytes using the URL safe base64 alphabet."""
    token = base64.urlsafe_b64encode(raw)
    if not padded:
        token = token.rstrip(b'=')
    return token.decode('ascii')


def decode_urlsafe(text):
    """Decode URL safe base64 text, restoring omitted padding."""
    text = text.strip()
    padding = (-len(text)) % 4
    return base64.urlsafe_b64decode(text + '=' * padding)


def is_urlsafe_alphabet(text):
    """Check that text only uses the URL safe base64 alphabet."""
    allowed = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_=')
    return all(char in allowed for char in text)


__all__ = ['encode_urlsafe', 'decode_urlsafe', 'is_urlsafe_alphabet']
