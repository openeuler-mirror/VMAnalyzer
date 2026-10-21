"""Look up disk cache mode implications for a libvirt cache setting.

Cache mode affects durability and migration compatibility.  Encoding the
documented implications in one table prevents inconsistent advice across
diagnostic checks.
"""

import logging
from typing import Dict, Optional

LOG = logging.getLogger(__name__)

CACHE_MODES: Dict[str, Dict[str, object]] = {
    "none": {"durable": True, "migration_safe": True, "host_cache": False},
    "writethrough": {"durable": True, "migration_safe": True, "host_cache": True},
    "writeback": {"durable": False, "migration_safe": True, "host_cache": True},
    "directsync": {"durable": True, "migration_safe": True, "host_cache": False},
    "unsafe": {"durable": False, "migration_safe": False, "host_cache": True},
    "default": {"durable": False, "migration_safe": True, "host_cache": True},
}


def describe(mode: str) -> Optional[Dict[str, object]]:
    """Return the implication table for a cache mode, or None."""
    key = str(mode).strip().lower()
    details = CACHE_MODES.get(key)
    if details is None:
        LOG.warning("unknown disk cache mode %r", mode)
    return details


def is_durable(mode: str) -> bool:
    """Return True when the mode survives host power loss."""
    details = describe(mode)
    return bool(details and details["durable"])


def migration_blocking(modes: Dict[str, str]) -> Dict[str, str]:
    """Return disks whose cache mode blocks live migration."""
    blocked = {disk: mode for disk, mode in modes.items()
               if not (describe(mode) or {}).get("migration_safe", False)}
    if blocked:
        LOG.warning("%d disk(s) use migration-unsafe cache modes", len(blocked))
    return blocked


__all__ = ["CACHE_MODES", "describe", "is_durable", "migration_blocking"]
