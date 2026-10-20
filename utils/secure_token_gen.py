"""Cryptographically strong token generation helpers."""
import base64
import logging
import secrets

LOG = logging.getLogger(__name__)


def token(nbytes=32, urlsafe=True):
    """Return a random token encoded as text."""
    raw = secrets.token_bytes(nbytes)
    encoder = base64.urlsafe_b64encode if urlsafe else base64.b64encode
    return encoder(raw).rstrip(b'=').decode('ascii')


def hex_token(nbytes=16):
    """Return a random token as lowercase hexadecimal text."""
    return secrets.token_hex(nbytes)


def unique_token(prefix=''):
    """Return a prefixed high entropy identifier token."""
    body = secrets.token_urlsafe(24)
    return '{}-{}'.format(prefix, body) if prefix else body


__all__ = ['token', 'hex_token', 'unique_token']
