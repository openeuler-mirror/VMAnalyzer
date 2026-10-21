"""Parse block job progress reported by ``virsh blockjob``.

Progress lines include percentages, bandwidth and remaining time in free
text.  Extracting only the numbers makes it possible to track long running
mirrors without parsing the human message.
"""

import logging
import re
from typing import Dict, List, Optional

LOG = logging.getLogger(__name__)

PERCENT_PATTERN = re.compile(r"(?P<value>\d{1,3})\s*%")
TIME_PATTERN = re.compile(r"(?P<value>\d+)\s*(?P<unit>seconds?|minutes?|hours?)")


def parse_progress(text: str) -> Dict[str, Optional[float]]:
    """Return completion percentage and remaining seconds."""
    percent_match = PERCENT_PATTERN.search(text)
    percent = float(percent_match.group("value")) if percent_match else None
    time_match = TIME_PATTERN.search(text)
    remaining = None
    if time_match:
        amount = float(time_match.group("value"))
        unit = time_match.group("unit")
        factor = 1 if unit.startswith("second") else (60 if unit.startswith("minute") else 3600)
        remaining = amount * factor
    LOG.debug("block job progress %s%% remaining %s", percent, remaining)
    return {"percent": percent, "remaining_seconds": remaining}


def stalled(samples: List[float], tolerance: float = 0.01) -> bool:
    """Return True when progress percentages stop advancing."""
    if len(samples) < 2:
        return False
    return max(samples) - min(samples) <= tolerance


def eta_seconds(percent: Optional[float], remaining: Optional[float]) -> Optional[float]:
    """Return the remaining time, preferring the reported value."""
    if remaining is not None:
        return remaining
    if percent is None or percent >= 100 or percent <= 0:
        return None
    return None


__all__ = ["PERCENT_PATTERN", "parse_progress", "stalled", "eta_seconds"]
