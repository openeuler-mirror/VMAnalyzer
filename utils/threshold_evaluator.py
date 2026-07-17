#!/usr/bin/env python3
"""Threshold evaluator with hysteresis to prevent alert flapping for VM metrics."""
from typing import Dict, Optional, Tuple
from enum import Enum

class AlertState(Enum):
    """Represents the current alert state for a metric."""
    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"

class ThresholdEvaluator:
    """Evaluates metric values against thresholds with hysteresis bands."""

    def __init__(self):
        self._thresholds: Dict[str, dict] = {}
        self._states: Dict[str, AlertState] = {}

    def set_threshold(self, metric: str, warning_high: float,
                      critical_high: float, warning_low: Optional[float] = None,
                      critical_low: Optional[float] = None,
                      hysteresis: float = 0.05) -> None:
        """Configure thresholds with optional hysteresis band."""
        self._thresholds[metric] = {
            "warning_high": warning_high,
            "critical_high": critical_high,
            "warning_low": warning_low if warning_low is not None else warning_high * (1 - hysteresis),
            "critical_low": critical_low if critical_low is not None else critical_high * (1 - hysteresis),
            "hysteresis": hysteresis,
        }
        if metric not in self._states:
            self._states[metric] = AlertState.NORMAL

    def evaluate(self, metric: str, value: float) -> AlertState:
        """Evaluate a metric value and return the resulting alert state."""
        if metric not in self._thresholds:
            raise KeyError(f"No thresholds configured for metric '{metric}'")
        config = self._thresholds[metric]
        current = self._states[metric]

        if value >= config["critical_high"]:
            new_state = AlertState.CRITICAL
        elif value >= config["warning_high"]:
            if current == AlertState.CRITICAL and value > config["critical_low"]:
                new_state = AlertState.CRITICAL
            else:
                new_state = AlertState.WARNING
        elif value <= config["warning_low"] and current == AlertState.WARNING:
            new_state = AlertState.NORMAL
        elif value <= config["critical_low"] and current == AlertState.CRITICAL:
            new_state = AlertState.WARNING
        elif current == AlertState.NORMAL:
            new_state = AlertState.NORMAL
        else:
            new_state = current

        self._states[metric] = new_state
        return new_state

    def get_state(self, metric: str) -> Optional[AlertState]:
        """Return the current alert state for a metric."""
        return self._states.get(metric)

    def reset(self, metric: str) -> None:
        """Reset the alert state for a metric to normal."""
        if metric in self._states:
            self._states[metric] = AlertState.NORMAL

    def get_config(self, metric: str) -> Optional[dict]:
        """Return the threshold configuration for a metric."""
        return self._thresholds.get(metric)

    def list_metrics(self) -> list:
        """Return list of all configured metrics."""
        return list(self._thresholds.keys())
