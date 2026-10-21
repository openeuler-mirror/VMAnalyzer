"""Hex encode and decode bytes with optional grouping and prefixes.

Artifact digests and guest identifiers are frequently exchanged as hex
strings.  Accepting separators, prefixes and mixed case when decoding
removes a common source of manual copy errors.
"""

import logging
import re
from typing import Iterable

LOG = logging.getLogger(__name__)

SEPARATOR_PATTERN = re.compile(r"[^0-9a-fA-F]")


def encode_hex(payload: bytes, upper: bool = False, grouped: int = 0) -> str:
    """Return the hex representation, optionally grouped with spaces."""
    text = payload.hex()
    if upper:
        text = text.upper()
    if grouped > 0:
        chunks: Iterable[str] = (text[index:index + grouped]
                                 for index in range(0, len(text), grouped))
        text = " ".join(chunks)
    LOG.debug("encoded %d byte(s) into %d hex character(s)", len(payload), len(text))
    return text


def decode_hex(text: str) -> bytes:
    """Decode hex text, ignoring spaces, colons and ``0x`` prefixes."""
    cleaned = SEPARATOR_PATTERN.sub("", text)
    if len(cleaned) % 2:
        raise ValueError("hex input must contain an even number of digits")
    return bytes.fromhex(cleaned)


def looks_like_hex(text: str) -> bool:
    """Return True when the text is a plausible hex payload."""
    cleaned = SEPARATOR_PATTERN.sub("", text)
    return bool(cleaned) and len(cleaned) % 2 == 0


__all__ = ["encode_hex", "decode_hex", "looks_like_hex"]
