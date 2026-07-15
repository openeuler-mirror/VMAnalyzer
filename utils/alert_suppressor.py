#!/usr/bin/env python3
"""Suppress duplicate alerts to reduce noise."""
import time
from typing import Dict, Optional

class AlertSuppressor:
    """Suppresses duplicate alerts within a time window."""

    def __init__(self, suppress_seconds: float = 300.0):
        self._suppress_window = suppress_seconds
        self._last_alert: Dict[str, float] = {}
        self._counts: Dict[str, int] = {}

    def should_suppress(self, alert_key: str) -> bool:
        """Check if an alert should be suppressed."""
        now = time.time()
        last = self._last_alert.get(alert_key, 0)
        if now - last < self._suppress_window:
            self._counts[alert_key] = self._counts.get(alert_key, 0) + 1
            return True
        self._last_alert[alert_key] = now
        self._counts[alert_key] = 1
        return False

    def suppress_count(self, alert_key: str) -> int:
        """Return how many times an alert was suppressed."""
        return self._counts.get(alert_key, 0)

    def reset(self, alert_key: str) -> None:
        """Reset suppression for an alert."""
        self._last_alert.pop(alert_key, None)
        self._counts.pop(alert_key, None)
