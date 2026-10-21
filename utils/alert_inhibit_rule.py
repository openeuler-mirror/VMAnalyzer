"""Apply inhibition rules that mute lower severity alerts during outages.

When a host is unreachable, every dependent VM alert fires as well.  A
simple rule table suppresses the derived alerts while the root alert is
active, reducing noise without losing the root cause.
"""

import logging
from typing import Dict, Iterable, List, Set

LOG = logging.getLogger(__name__)

SEVERITY_RANK = {"info": 1, "warning": 2, "error": 3, "critical": 4}


def is_active(alert: Dict[str, object]) -> bool:
    """Return True when an alert record is firing."""
    return str(alert.get("state", alert.get("status", "firing"))).lower() == "firing"


def rank(alert: Dict[str, object]) -> int:
    """Return the numeric severity rank of an alert."""
    return SEVERITY_RANK.get(str(alert.get("severity", "info")).lower(), 1)


def inhibit(alerts: Iterable[Dict[str, object]],
            rules: Dict[str, Set[str]]) -> List[Dict[str, object]]:
    """Drop alerts inhibited by an active alert of a named category."""
    materialised = list(alerts)
    active_targets = {
        str(alert.get("root_cause"))
        for alert in materialised
        if is_active(alert) and alert.get("root_cause")
    }
    kept: List[Dict[str, object]] = []
    muted = 0
    for alert in materialised:
        category = str(alert.get("category", ""))
        source = str(alert.get("root_cause", ""))
        if source and source in active_targets and category in rules.get(source, set()):
            muted += 1
            continue
        kept.append(alert)
    if muted:
        LOG.info("inhibited %d dependent alert(s)", muted)
    return kept


__all__ = ["SEVERITY_RANK", "is_active", "rank", "inhibit"]
