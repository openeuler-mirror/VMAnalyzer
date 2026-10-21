"""Compute the classic 32-bit FNV-1 hash of bytes.

FNV-1 (multiply then XOR) is used by several file format specs and differs
from FNV-1a only in operation order.  Keeping both variants explicit avoids
accidental hash mismatches during format validation.
"""

import logging

LOG = logging.getLogger(__name__)

OFFSET_BASIS = 0x811C9DC5
PRIME = 0x01000193


def fnv1_32(payload: bytes) -> int:
    """Return the 32-bit FNV-1 hash of *payload*."""
    digest = OFFSET_BASIS
    for byte in payload:
        digest = (digest * PRIME) & 0xFFFFFFFF
        digest ^= byte
    LOG.debug("FNV-1 hash computed over %d byte(s)", len(payload))
    return digest


def fnv1a_32(payload: bytes) -> int:
    """Return the 32-bit FNV-1a hash for comparison and validation."""
    digest = OFFSET_BASIS
    for byte in payload:
        digest ^= byte
        digest = (digest * PRIME) & 0xFFFFFFFF
    return digest


def fnv1_32_hex(payload: bytes) -> str:
    """Return the FNV-1 hash as zero-padded lowercase hex."""
    return "{:08x}".format(fnv1_32(payload))


__all__ = ["OFFSET_BASIS", "PRIME", "fnv1_32", "fnv1a_32", "fnv1_32_hex"]
