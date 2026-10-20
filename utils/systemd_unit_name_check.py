"""Validate systemd unit names and derive their type suffixes."""

import re

_TYPES = ("service", "socket", "timer", "target", "mount", "automount",
          "swap", "path", "slice", "scope", "device")
_NAME = re.compile(r"^[A-Za-z0-9:_.\\-]+$")


def is_valid_unit_name(name):
    """Return True when a unit name is structurally valid for systemd."""
    if not name or len(name) > 255 or "/" in name or name.startswith("."):
        return False
    return bool(_NAME.match(name)) and "." in name


def unit_type(name):
    """Return the unit type suffix, or ``None`` when absent or unknown."""
    if "." not in (name or ""):
        return None
    suffix = name.rsplit(".", 1)[1].lower()
    return suffix if suffix in _TYPES else None


def is_template(name):
    """Return True when the unit name uses the ``@`` instance template form."""
    return "@" in (name or "")


def instance_of(name, instance):
    """Render a template unit with a concrete instance substituted in."""
    if not is_template(name):
        return name
    base, _, suffix = name.partition("@")
    return "{}@{}.{}".format(base, instance, suffix.split(".", 1)[-1])


__all__ = ["is_valid_unit_name", "unit_type", "is_template", "instance_of"]
