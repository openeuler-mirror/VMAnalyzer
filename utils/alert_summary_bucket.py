"""Bucket alerts into per-host per-severity summary rows.

Dashboards need one row per host and severity rather than the full alert
list.  Aggregating early reduces payload size and keeps rendering time
constant regardless of alert volume.
"""

import logging
from typing import Dict, Iterable, List

LOG = logging.getLogger(__name__)


def bucket(alerts: Iterable[Dict[str, object]]) -> List[Dict[str, object]]:
    """Aggregate alerts into sorted host/severity summary rows."""
    groups: Dict[tuple, Dict[str, int]] = {}
    for alert in alerts:
        key = (str(alert.get("host", "unknown")), str(alert.get("severity", "info")))
        entry = groups.setdefault(key, {"count": 0, "firing": 0})
        entry["count"] += 1
        if str(alert.get("state", "firing")) == "firing":
            entry["firing"] += 1
    rows = [
        {"host": host, "severity": severity,
         "count": values["count"], "firing": values["firing"]}
        for (host, severity), values in groups.items()
    ]
    rows.sort(key=lambda row: (row["host"], row["severity"]))
    LOG.debug("summarised alerts into %d bucket row(s)", len(rows))
    return rows


def totals(rows: List[Dict[str, object]]) -> Dict[str, int]:
    """Sum counts and firing totals across summary rows."""
    return {
        "count": sum(int(row["count"]) for row in rows),
        "firing": sum(int(row["firing"]) for row in rows),
    }


__all__ = ["bucket", "totals"]
