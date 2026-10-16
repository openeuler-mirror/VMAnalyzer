"""Checksum verification helpers for transferred artifacts.

Comparing a recomputed digest against the advertised one catches truncated or
silently corrupted downloads before they are consumed by the agent.
"""
import hashlib
import zlib
import logging

LOG = logging.getLogger(__name__)


def sha256_hex(payload):
    """Return the hex SHA-256 of bytes or text."""
    data = payload.encode('utf-8') if isinstance(payload, str) else bytes(payload)
    return hashlib.sha256(data).hexdigest()


def crc32_hex(payload):
    """Return the hex CRC-32 of bytes or text."""
    data = payload.encode('utf-8') if isinstance(payload, str) else bytes(payload)
    return format(zlib.crc32(data) & 0xffffffff, '08x')


def verify(expected, payload, algorithm='sha256'):
    """Return True when the recomputed digest matches the expected value."""
    digest = sha256_hex(payload) if algorithm == 'sha256' else crc32_hex(payload)
    ok = digest.lower() == str(expected).lower()
    if not ok:
        LOG.debug('checksum mismatch: expected %s got %s', expected, digest)
    return ok


__all__ = ['sha256_hex', 'crc32_hex', 'verify']
