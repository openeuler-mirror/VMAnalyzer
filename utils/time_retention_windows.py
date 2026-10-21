"""Translate a retention policy into concrete cut-off timestamps.

Storage layers need a single cut-off, while operators think in tiers such
as "keep hourly for two days, daily for a month".  This module converts the
tier description into sorted boundaries used by sweep jobs.
"""

import logging
import time
from typing import Dict, List, Tuple

LOG = logging.getLogger(__name__)

DEFAULT_TIERS = (("raw", 2, 86400), ("hourly", 30, 86400), ("daily", 365, 86400))


def cutoff_timestamps(tiers=DEFAULT_TIERS, now: float = None) -> Dict[str, float]:
    """Return the oldest timestamp to keep per retention tier."""
    reference = time.time() if now is None else now
    cutoffs: Dict[str, float] = {}
    for name, span, unit_seconds in tiers:
        cutoffs[name] = float(reference - span * unit_seconds)
    LOG.debug("computed %d retention cut-off(s)", len(cutoffs))
    return cutoffs


def bucket_for_age(age_seconds: float, tiers=DEFAULT_TIERS) -> str:
    """Return the finest tier that still covers the given age."""
    ordered: List[Tuple[str, float]] = sorted(
        ((name, span * unit_seconds) for name, span, unit_seconds in tiers),
        key=lambda item: item[1],
    )
    for name, limit in ordered:
        if age_seconds <= limit:
            return name
    return "expired"


def expired_names(cutoffs: Dict[str, float], oldest_kept: float) -> List[str]:
    """List tiers whose cut-off is newer than the oldest known sample."""
    names = [name for name, cutoff in cutoffs.items() if cutoff > oldest_kept]
    if names:
        LOG.info("tiers with no surviving samples: %s", ", ".join(sorted(names)))
    return sorted(names)


__all__ = ["DEFAULT_TIERS", "cutoff_timestamps", "bucket_for_age", "expired_names"]
