"""Normalize MAC addresses from the many textual spellings to one canonical form."""

import re

_DIGITS = re.compile(r"[0-9A-Fa-f]{2}")


def extract_mac_octets(text):
    """Return the eight hex digits of a MAC address found in arbitrary text."""
    digits = "".join(_DIGITS.findall(text.replace("-", ":").replace(".", ":")))
    return digits if len(digits) == 12 else None


def normalize_mac(text, separator=":", upper=False):
    """Return the canonical MAC string or ``None`` when the input is malformed."""
    digits = extract_mac_octets(text)
    if digits is None:
        return None
    pieces = [digits[i:i + 2] for i in range(0, 12, 2)]
    rendered = separator.join(pieces)
    return rendered.upper() if upper else rendered.lower()


def mac_is_local(text):
    """Return True when the MAC address has the locally-administered bit set."""
    digits = extract_mac_octets(text)
    if digits is None:
        return False
    return bool(int(digits[0:2], 16) & 0x02)


__all__ = ["extract_mac_octets", "normalize_mac", "mac_is_local"]
