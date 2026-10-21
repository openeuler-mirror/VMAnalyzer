"""Compare guest CPU feature flags against the host model.

A guest missing host features such as ``aes`` or ``avx2`` runs slower than
expected.  Reporting the difference between host and guest flag lists
pinpoints configuration drift without inspecting the domain XML manually.
"""

import logging
from typing import Dict, Iterable, List

LOG = logging.getLogger(__name__)


def parse_flags(text: str) -> List[str]:
    """Split a CPU flag string into a normalised sorted list."""
    return sorted({token.strip().lower() for token in text.replace("\n", " ").split()
                   if token.strip()})


def compare(host_flags: Iterable[str], guest_flags: Iterable[str]) -> Dict[str, List[str]]:
    """Return host-only, guest-only and shared CPU flags."""
    host = set(flags.lower() for flags in host_flags)
    guest = set(flags.lower() for flags in guest_flags)
    result = {
        "host_only": sorted(host - guest),
        "guest_only": sorted(guest - host),
        "shared": sorted(host & guest),
    }
    LOG.debug("CPU flag diff: %d host-only, %d guest-only",
              len(result["host_only"]), len(result["guest_only"]))
    return result


def missing_important(host_flags: Iterable[str], guest_flags: Iterable[str],
                      important: Iterable[str] = ("aes", "avx", "avx2", "sse4_2")) -> List[str]:
    """Return important host features absent from the guest."""
    diff = compare(host_flags, guest_flags)
    missing = [flag for flag in important if flag in diff["host_only"]]
    if missing:
        LOG.info("guest lacks important CPU feature(s): %s", ", ".join(missing))
    return missing


__all__ = ["parse_flags", "compare", "missing_important"]
