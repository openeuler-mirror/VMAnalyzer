"""Risk tag merge helper."""

from __future__ import annotations

from typing import Iterable


def merge_tags(*groups: Iterable[str]) -> list[str]:
    result = []
    seen = set()
    for group in groups:
        for tag in group:
            if tag not in seen:
                seen.add(tag)
                result.append(tag)
    return result

