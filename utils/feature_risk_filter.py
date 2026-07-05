"""Risk filter helper."""

from __future__ import annotations

from typing import Iterable, Mapping


def filter_by_risk(items: Iterable[Mapping[str, object]], tag: str) -> list[Mapping[str, object]]:
    return [item for item in items if tag in item.get("risk_tags", [])]

