"""Guess the guest OS family from os-release style key-value text.

Diagnostics produce different advice for RHEL, Debian and SUSE families.
Reading the identity keys is sufficient for most checks and avoids running
commands inside the guest just to classify the distribution.
"""

import logging
from typing import Dict, Optional

LOG = logging.getLogger(__name__)

FAMILY_HINTS = {
    "rhel": ("rhel", "centos", "fedora", "openEuler", "anolis", "kylin", "openeuler"),
    "debian": ("debian", "ubuntu"),
    "suse": ("suse", "sles", "opensuse"),
    "arch": ("arch", "manjaro"),
}


def parse_os_release(text: str) -> Dict[str, str]:
    """Parse ``KEY=value`` lines from os-release content."""
    fields: Dict[str, str] = {}
    for line in text.splitlines():
        key, separator, value = line.strip().partition("=")
        if not separator or key.startswith("#"):
            continue
        fields[key.strip()] = value.strip().strip("\"'")
    return fields


def guess_family(text: str) -> Optional[str]:
    """Return the OS family name, or None when it cannot be determined."""
    fields = parse_os_release(text)
    identity = " ".join([fields.get("ID", ""), fields.get("ID_LIKE", ""),
                        fields.get("NAME", "")]).lower()
    for family, hints in FAMILY_HINTS.items():
        if any(hint.lower() in identity for hint in hints):
            LOG.debug("guest identified as %s family", family)
            return family
    LOG.warning("cannot guess the OS family from os-release")
    return None


__all__ = ["FAMILY_HINTS", "parse_os_release", "guess_family"]
