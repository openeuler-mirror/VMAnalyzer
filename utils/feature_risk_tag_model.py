"""Risk tag model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskTag:
    name: str
    severity: str = "warning"
    detail: str = ""

