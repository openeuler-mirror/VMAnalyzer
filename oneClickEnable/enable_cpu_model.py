"""Canonical names for the cpu model values reported by libvirt.

Libvirt, QEMU and the kernel disagree on spelling for the same setting.  A
single canonical table with a reverse index keeps every report comparable.
"""

import logging

LOG = logging.getLogger(__name__)

CANONICAL = {
    "auto": "auto",
    "none": "none",
    "on": "on",
    "off": "off",
    "default": "default",
    "safe": "safe",
}

ALIASES = {
    "yes": "on",
    "no": "off",
    "true": "on",
    "false": "off",
    "null": "none",
}


def canonical(value, default="auto"):
    """Map a raw cpu model value onto the canonical spelling."""
    raw = str(value or "").strip().lower()
    raw = ALIASES.get(raw, raw)
    if raw in CANONICAL:
        return CANONICAL[raw]
    LOG.debug("unknown cpu_model value %r, using %s", value, default)
    return default


def reverse(value):
    """Return every alias that maps onto the canonical *value*."""
    return sorted(alias for alias, target in ALIASES.items()
                  if target == value)


def normalise(mapping):
    """Return a copy of *mapping* with every value put in canonical form."""
    return {key: canonical(value) for key, value in (mapping or {}).items()}


__all__ = ["canonical", "reverse", "normalise"]
