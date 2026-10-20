"""Parse human friendly memory size strings such as ``1.5Gi`` into bytes."""

import re

_UNITS = {"b": 1, "k": 1000, "kb": 1000, "m": 1000 ** 2, "mb": 1000 ** 2,
          "g": 1000 ** 3, "gb": 1000 ** 3, "t": 1000 ** 4, "tb": 1000 ** 4,
          "ki": 1024, "kib": 1024, "mi": 1024 ** 2, "mib": 1024 ** 2,
          "gi": 1024 ** 3, "gib": 1024 ** 3, "ti": 1024 ** 4, "tib": 1024 ** 4}

_PATTERN = re.compile(r"^\s*([0-9]+(?:\.[0-9]+)?)\s*([A-Za-z]*)\s*$")


def parse_size(text):
    """Return the size in bytes, or ``None`` when the string is not recognized."""
    match = _PATTERN.match(text or "")
    if not match:
        return None
    number = float(match.group(1))
    unit = (match.group(2) or "b").lower()
    if unit not in _UNITS:
        return None
    return int(number * _UNITS[unit])


def parse_size_or(text, default=0):
    """Return the parsed byte count or a caller supplied default."""
    value = parse_size(text)
    return default if value is None else value


def format_size(num_bytes, precision=1):
    """Render a byte count using binary units with a trailing ``i``."""
    value = float(num_bytes)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if value < 1024 or unit == "TiB":
            return "{:.{}f}{}".format(value, precision, unit)
        value /= 1024
    return "{}B".format(num_bytes)


__all__ = ["parse_size", "parse_size_or", "format_size"]
