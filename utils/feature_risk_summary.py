"""Risk summary helper."""

from __future__ import annotations

from collections import Counter
from typing import Iterable


def summarize_risk_tags(tags: Iterable[str]) -> dict[str, int]:
    return dict(Counter(tags))

