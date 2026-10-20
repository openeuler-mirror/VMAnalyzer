"""Parse fstab option strings such as ``rw,noatime,size=10%`` into a mapping."""

import re

_KEY_VALUE = re.compile(r"^([A-Za-z0-9_]+)=(.+)$")


def parse_fstab_options(options):
    """Return ``(flags, values)`` split from a comma separated option string."""
    flags = set()
    values = {}
    for token in (options or "").split(","):
        token = token.strip()
        if not token:
            continue
        match = _KEY_VALUE.match(token)
        if match:
            values[match.group(1).lower()] = match.group(2)
        else:
            flags.add(token.lower())
    return flags, values


def has_option(options, name):
    """Return True when a boolean or keyed option is present."""
    flags, values = parse_fstab_options(options)
    return name.lower() in flags or name.lower() in values


def option_value(options, name, default=None):
    """Return the value of a keyed option, or ``default``."""
    _, values = parse_fstab_options(options)
    return values.get(name.lower(), default)


def is_read_only(options):
    """Return True when the mount options disable write access."""
    flags, _ = parse_fstab_options(options)
    return "ro" in flags


__all__ = ["parse_fstab_options", "has_option", "option_value", "is_read_only"]
