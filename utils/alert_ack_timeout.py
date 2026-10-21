"""Find acknowledged alerts whose acknowledgement has expired.

Acknowledgements are meant to silence an alert for a bounded time.  When
the window passes with the condition still firing, the alert must return to
the active queue rather than remain silently acknowledged.
"""

import logging
import time
from typing import Dict, Iterable, List

LOG = logging.getLogger(__name__)


def expired_acknowledgements(alerts: Iterable[Dict[str, object]],
                             timeout: float = 3600.0,
                             now: float = None) -> List[Dict[str, object]]:
    """Return still-firing alerts whose acknowledgement has lapsed."""
    reference = time.time() if now is None else now
    expired: List[Dict[str, object]] = []
    for alert in alerts:
        if not alert.get("acknowledged_at"):
            continue
        if str(alert.get("state", "firing")) != "firing":
            continue
        if reference - float(alert["acknowledged_at"]) >= timeout:
            expired.append(alert)
    if expired:
        LOG.info("%d acknowledgement(s) expired while still firing", len(expired))
    return expired


def remaining(alerts: Iterable[Dict[str, object]], timeout: float = 3600.0,
              now: float = None) -> Dict[str, float]:
    """Return how long each acknowledged alert remains silenced."""
    reference = time.time() if now is None else now
    result: Dict[str, float] = {}
    for alert in alerts:
        acknowledged = alert.get("acknowledged_at")
        if not acknowledged:
            continue
        name = str(alert.get("name", alert.get("fingerprint", "")))
        result[name] = max(0.0, timeout - (reference - float(acknowledged)))
    return result


__all__ = ["expired_acknowledgements", "remaining"]
