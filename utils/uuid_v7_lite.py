"""Generate time-ordered UUIDv7 identifiers without external packages.

UUIDv7 keeps a millisecond timestamp in the high bits so identifiers sort
chronologically, which is valuable for event tables.  This implementation
keeps the standard layout while allowing deterministic randomness in tests.
"""

import logging
import os
import time
import uuid
from typing import Optional

LOG = logging.getLogger(__name__)


def uuid7(timestamp_ms: Optional[int] = None, random_bits: Optional[int] = None) -> uuid.UUID:
    """Return a UUIDv7 with the supplied or current millisecond timestamp."""
    milliseconds = int(time.time() * 1000) if timestamp_ms is None else int(timestamp_ms)
    if milliseconds < 0:
        raise ValueError("timestamp must not be negative")
    if random_bits is None:
        random_bits = int.from_bytes(os.urandom(10), "big")
    random_bits &= (1 << 74) - 1
    value = (milliseconds & ((1 << 48) - 1)) << 80
    value |= 0x7 << 76
    value |= (random_bits >> 62) & 0xFFF << 64
    value |= 0b10 << 62
    value |= random_bits & ((1 << 62) - 1)
    LOG.debug("generated uuid7 for timestamp %d", milliseconds)
    return uuid.UUID(int=value)


def timestamp_of(identifier: uuid.UUID) -> int:
    """Extract the millisecond timestamp embedded in a UUIDv7."""
    return identifier.int >> 80


def is_uuid7(identifier: uuid.UUID) -> bool:
    """Check the version nibble of a UUID instance."""
    return identifier.version == 7


__all__ = ["uuid7", "timestamp_of", "is_uuid7"]
