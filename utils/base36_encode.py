"""Encode integers with the URL-safe base36 alphabet.

Short identifiers for VMs and jobs must stay readable and sortable-ish in
logs.  Base36 uses digits plus lowercase letters, avoiding the ambiguous
symbols that base62 introduces while keeping identifiers compact.
"""

import logging
from typing import Optional

LOG = logging.getLogger(__name__)

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"


def encode_base36(number: int) -> str:
    """Encode a non-negative integer into base36."""
    if number < 0:
        raise ValueError("base36 encoding requires a non-negative integer")
    if number == 0:
        return "0"
    digits = []
    value = number
    while value:
        value, remainder = divmod(value, len(ALPHABET))
        digits.append(ALPHABET[remainder])
    encoded = "".join(reversed(digits))
    LOG.debug("encoded %d into %s", number, encoded)
    return encoded


def decode_base36(text: str) -> int:
    """Decode a base36 string back into an integer."""
    if not text:
        raise ValueError("cannot decode an empty base36 string")
    value = 0
    for char in text.lower():
        position = ALPHABET.find(char)
        if position < 0:
            raise ValueError("invalid base36 character: {!r}".format(char))
        value = value * len(ALPHABET) + position
    return value


def fixed_width(number: int, width: int) -> Optional[str]:
    """Encode with left padding, or return None when it cannot fit."""
    encoded = encode_base36(number)
    if len(encoded) > width:
        LOG.warning("value %d does not fit into %d base36 digits", number, width)
        return None
    return encoded.rjust(width, "0")


__all__ = ["ALPHABET", "encode_base36", "decode_base36", "fixed_width"]
