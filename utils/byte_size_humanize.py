"""Format byte counts as human-readable strings and back again."""
__all__ = ["humanize_bytes", "parse_size"]

_UNITS = ("B", "KiB", "MiB", "GiB", "TiB", "PiB")
_FACTORS = {
    "b": 1, "kb": 1000, "kib": 1024, "mb": 1000 ** 2,
    "mib": 1024 ** 2, "gb": 1000 ** 3, "gib": 1024 ** 3,
}


def humanize_bytes(size, precision=1):
    """Return *size* bytes rendered with the largest fitting binary unit."""
    value = float(size)
    for unit in _UNITS:
        if abs(value) < 1024 or unit == _UNITS[-1]:
            return "%.*f %s" % (precision, value, unit)
        value /= 1024
    return "%.*f %s" % (precision, value, _UNITS[-1])


def parse_size(text):
    """Parse strings such as ``1.5 MiB`` back into an integer byte count."""
    token = str(text).strip().replace(" ", "").lower()
    number = "".join(c for c in token if c.isdigit() or c == ".")
    unit = token[len(number):]
    return int(float(number) * _FACTORS.get(unit or "b", 1))
