"""Estimate the memory headroom a guest needs to avoid swapping.

Headroom should scale with the guest's working set, not its maximum size.
Combining available memory, committed memory and a safety factor gives a
stable low-water mark for the balloon controller.
"""

import logging
from typing import Dict

LOG = logging.getLogger(__name__)


def headroom_bytes(total: int, available: int, committed: int,
                   safety: float = 0.15) -> int:
    """Return the recommended free memory floor in bytes."""
    if total <= 0:
        return 0
    reserve = int(max(committed * safety, total * 0.05))
    floor = min(available, reserve)
    LOG.debug("memory headroom %d bytes for %d byte guest", floor, total)
    return floor


def pressure_state(total: int, available: int, committed: int) -> str:
    """Classify guest memory pressure into a coarse state."""
    if total <= 0:
        return "unknown"
    ratio = available / total
    if ratio < 0.05 or available < committed * 0.1:
        return "critical"
    if ratio < 0.15:
        return "warning"
    return "ok"


def summary(total: int, available: int, committed: int) -> Dict[str, object]:
    """Return headroom and pressure state together."""
    result = {
        "headroom": headroom_bytes(total, available, committed),
        "state": pressure_state(total, available, committed),
        "available_ratio": round(available / total, 4) if total else 0.0,
    }
    if result["state"] != "ok":
        LOG.warning("guest memory pressure is %s", result["state"])
    return result


__all__ = ["headroom_bytes", "pressure_state", "summary"]
