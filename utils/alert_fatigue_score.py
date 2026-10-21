"""Score alert streams for fatigue using volume, duplication and churn.

Operators ignore alerting when most pages repeat the same condition.
Combining volume, duplicate ratio and short-lived alerts into one score
makes the problem measurable and trackable over time.
"""

import logging
from typing import Dict, Iterable, Tuple

LOG = logging.getLogger(__name__)


def duplicate_ratio(alerts: Iterable[Tuple[str, float]]) -> float:
    """Return the share of alerts whose fingerprint repeats."""
    materialised = list(alerts)
    if not materialised:
        return 0.0
    unique = {fingerprint for fingerprint, _ in materialised}
    return 1.0 - len(unique) / len(materialised)


def flapping_ratio(alerts: Iterable[Tuple[str, float]], lifetime: float = 60.0) -> float:
    """Return the share of alerts that resolved within *lifetime* seconds."""
    materialised = list(alerts)
    if not materialised:
        return 0.0
    short = sum(1 for _, duration in materialised if duration < lifetime)
    return short / len(materialised)


def fatigue_score(alerts: Iterable[Tuple[str, float]], volume_target: int = 50) -> Dict[str, float]:
    """Combine volume, duplication and flapping into a 0-100 score."""
    materialised = list(alerts)
    volume = min(1.0, len(materialised) / float(max(1, volume_target)))
    duplicates = duplicate_ratio(materialised)
    flapping = flapping_ratio(materialised)
    score = round((0.4 * volume + 0.35 * duplicates + 0.25 * flapping) * 100.0, 2)
    if score >= 60:
        LOG.warning("alert fatigue score %.1f suggests noisy rules", score)
    return {"score": score, "volume": round(volume, 3),
            "duplicate_ratio": round(duplicates, 3), "flapping_ratio": round(flapping, 3)}


__all__ = ["duplicate_ratio", "flapping_ratio", "fatigue_score"]
