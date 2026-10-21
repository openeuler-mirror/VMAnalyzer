"""Translate cgroup CPU quota settings into effective CPU counts.

cgroup v1 exposes ``cpu.cfs_quota_us`` and ``cpu.cfs_period_us`` separately.
Dividing them yields the CPU limit, and reporting both values keeps
debugging straightforward when the limit is fractional.
"""

import logging
from typing import Dict, Optional

LOG = logging.getLogger(__name__)

DEFAULT_PERIOD = 100000


def read_int(path: str) -> Optional[int]:
    """Return the integer content of a cgroup file, or None."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return int(handle.read().strip())
    except (OSError, ValueError) as error:
        LOG.warning("cannot read cgroup value from %s: %s", path, error)
        return None


def effective_cpus(quota: Optional[int], period: Optional[int]) -> Optional[float]:
    """Return the CPU limit implied by quota and period."""
    if quota is None or quota <= 0:
        return None
    divisor = period if period and period > 0 else DEFAULT_PERIOD
    return round(quota / divisor, 4)


def describe(quota: Optional[int], period: Optional[int]) -> Dict[str, object]:
    """Return a mapping describing the CPU bandwidth limit."""
    cpus = effective_cpus(quota, period)
    description = {
        "quota": quota,
        "period": period or DEFAULT_PERIOD,
        "cpus": cpus,
        "unlimited": cpus is None,
    }
    LOG.debug("cgroup cpu description %s", description)
    return description


__all__ = ["DEFAULT_PERIOD", "read_int", "effective_cpus", "describe"]
