"""Normalise pressure stall information into percentages.

PSI metrics report total stall microseconds per interval.  Dividing by the
interval duration gives the familiar "percent of time stalled" figure used
in capacity reports.
"""

import logging
from typing import Dict, Optional

LOG = logging.getLogger(__name__)


def stall_percent(stall_microseconds: float, interval_seconds: float) -> float:
    """Return the share of the interval spent stalled."""
    if interval_seconds <= 0:
        raise ValueError("interval_seconds must be positive")
    total = float(interval_seconds) * 1_000_000
    return round(min(100.0, float(stall_microseconds) / total * 100.0), 3)


def from_avg(avg10: float) -> Dict[str, float]:
    """Translate PSI ``avg10`` values into a compact threshold view."""
    value = max(0.0, min(100.0, float(avg10)))
    result = {"percent": value, "fraction": round(value / 100.0, 4)}
    if value >= 50:
        LOG.warning("pressure average is %.1f%%, sustained contention likely", value)
    return result


def classify(total: Optional[float], some: Optional[float],
             full: Optional[float]) -> str:
    """Classify memory pressure using the PSI total/some/full triple."""
    if full is not None and full >= 10.0:
        return "critical"
    if some is not None and some >= 50.0:
        return "warning"
    if total is not None and total >= 90.0:
        return "warning"
    return "ok"


__all__ = ["stall_percent", "from_avg", "classify"]
