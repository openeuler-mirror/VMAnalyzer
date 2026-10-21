"""Compute simple XOR-8 and additive checksums for short frames.

Some BMC and serial protocols use trivial checksums rather than CRCs.
These helpers keep verification in one place and reject frames whose
declared checksum byte disagrees with the payload.
"""

import logging

LOG = logging.getLogger(__name__)


def xor8(payload: bytes, seed: int = 0) -> int:
    """Return the XOR of every byte combined with *seed*."""
    value = seed & 0xFF
    for byte in payload:
        value ^= byte
    return value & 0xFF


def additive8(payload: bytes) -> int:
    """Return the low byte of the sum of all payload bytes."""
    return sum(payload) & 0xFF


def verify_frame(frame: bytes, algorithm: str = "xor") -> bool:
    """Verify the trailing checksum byte of a frame."""
    if len(frame) < 2:
        return False
    body, expected = frame[:-1], frame[-1]
    computed = xor8(body) if algorithm == "xor" else additive8(body)
    matches = computed == expected
    if not matches:
        LOG.warning("frame checksum mismatch, expected %02x got %02x", expected, computed)
    return matches


__all__ = ["xor8", "additive8", "verify_frame"]
