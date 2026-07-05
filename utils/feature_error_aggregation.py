"""Error aggregation helper."""

from __future__ import annotations

from collections import Counter
from typing import Iterable, Mapping


def count_by_type(errors: Iterable[Mapping[str, object]]) -> dict:
    return dict(Counter(str(error.get("type", "unknown")) for error in errors))

