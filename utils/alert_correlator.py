#!/usr/bin/env python3
"""Correlate related alert signals to reduce false positives."""
import time
from typing import Dict, List, Optional

class AlertCorrelator:
    """Correlates alerts that occur within a time window."""

    def __init__(self, correlation_window: float = 60.0):
        self._window = correlation_window
        self._groups: Dict[str, List] = {}

    def add_alert(self, source: str, alert_type: str,
                  timestamp: float = None) -> Optional[str]:
        """Add an alert and return correlation group if found."""
        ts = timestamp or time.time()
        for group_id, alerts in self._groups.items():
            recent = [a for a in alerts if ts - a[2] <= self._window]
            if any(a[0] != source and a[1] == alert_type for a in recent):
                alerts.append((source, alert_type, ts))
                return group_id
        group_id = f"{alert_type}_{int(ts)}"
        self._groups[group_id] = [(source, alert_type, ts)]
        return None

    def get_group(self, group_id: str) -> List:
        """Return alerts in a correlation group."""
        return self._groups.get(group_id, [])

    def cleanup(self) -> int:
        """Remove expired groups."""
        now = time.time()
        expired = [gid for gid, alerts in self._groups.items()
                   if all(now - a[2] > self._window for a in alerts)]
        for gid in expired:
            del self._groups[gid]
        return len(expired)
