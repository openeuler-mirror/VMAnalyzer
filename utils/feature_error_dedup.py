"""Error deduplication helper."""

from __future__ import annotations

from typing import Iterable, Mapping


def dedupe_errors(errors: Iterable[Mapping[str, object]]) -> list[Mapping[str, object]]:
    seen = set()
    result = []
    for error in errors:
        key = (error.get("type"), error.get("message"))
        if key in seen:
            continue
        seen.add(key)
        result.append(error)
    return result

