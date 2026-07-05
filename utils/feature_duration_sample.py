"""Collection duration sample model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DurationSample:
    name: str
    elapsed_seconds: float
    status: str = "ok"
    detail: str | None = None

