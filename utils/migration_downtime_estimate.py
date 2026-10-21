"""Estimate likely live migration downtime from bandwidth and dirty rate.

Downtime depends on the amount of dirtied memory during the final switch,
not on the total guest size.  The estimate helps decide whether post-copy
or a longer convergence window is required.
"""

import logging
from typing import Dict, Optional

LOG = logging.getLogger(__name__)


def final_dirty_bytes(dirty_rate_bps: float, switch_overhead: float) -> float:
    """Return the bytes dirtied during the switch-over window."""
    return max(0.0, dirty_rate_bps * switch_overhead)


def downtime_seconds(dirty_rate_bps: float, bandwidth_bps: float,
                     switch_overhead: float = 0.5) -> Optional[float]:
    """Return the projected downtime in seconds, or None if it cannot converge."""
    if bandwidth_bps <= 0:
        return None
    dirty = final_dirty_bytes(dirty_rate_bps, switch_overhead)
    available = bandwidth_bps - dirty_rate_bps
    if available <= 0:
        LOG.warning("migration cannot converge, dirty rate exceeds bandwidth")
        return None
    return round(dirty / available, 3)


def assess(dirty_rate_bps: float, bandwidth_bps: float,
           backlog_bytes: float = 0.0) -> Dict[str, object]:
    """Summarise convergence feasibility for a migration plan."""
    initial = round(backlog_bytes / bandwidth_bps, 2) if bandwidth_bps > 0 else None
    downtime = downtime_seconds(dirty_rate_bps, bandwidth_bps)
    result = {
        "initial_transfer_seconds": initial,
        "downtime_seconds": downtime,
        "converges": downtime is not None,
    }
    LOG.debug("migration assessment %s", result)
    return result


__all__ = ["final_dirty_bytes", "downtime_seconds", "assess"]
