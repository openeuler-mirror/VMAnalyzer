"""Slowest duration selector."""

from __future__ import annotations

from typing import Iterable, Mapping


def slowest(items: Iterable[Mapping[str, object]], limit: int = 5) -> list[Mapping[str, object]]:
    return sorted(items, key=lambda item: float(item.get("elapsed_seconds", 0.0)), reverse=True)[:limit]

