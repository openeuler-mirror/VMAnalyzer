"""Convert between hex digests and unpadded base32 notation.

Some inventory exports use base32 because it survives case-insensitive
copy/paste, while the source digests are hex.  Bridging both directions
keeps import pipelines independent of the export dialect.
"""

import base64
import binascii
import logging
from typing import Optional

LOG = logging.getLogger(__name__)


def hex_to_base32(hex_text: str) -> str:
    """Convert a hex digest into uppercase unpadded base32."""
    raw = binascii.unhexlify(hex_text.strip())
    encoded = base64.b32encode(raw).decode("ascii").rstrip("=")
    LOG.debug("converted %d hex char(s) into %d base32 char(s)", len(hex_text), len(encoded))
    return encoded


def base32_to_hex(text: str) -> str:
    """Convert base32 text back into lowercase hex."""
    cleaned = text.strip().upper().rstrip("=")
    padding = (-len(cleaned)) % 8
    raw = base64.b32decode(cleaned + "=" * padding, casefold=True)
    return raw.hex()


def try_convert(text: str) -> Optional[str]:
    """Return the converted value, or None when the input is malformed."""
    try:
        if all(char in "0123456789abcdefABCDEF" for char in text.strip()):
            return hex_to_base32(text)
        return base32_to_hex(text)
    except (binascii.Error, ValueError) as error:
        LOG.warning("conversion failed for %r: %s", text, error)
        return None


__all__ = ["hex_to_base32", "base32_to_hex", "try_convert"]
