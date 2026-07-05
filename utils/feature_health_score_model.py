"""Health score model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HealthScore:
    value: float
    level: str
    reason: str = ""

