"""Risk JSON export helper."""

from __future__ import annotations

import json
from typing import Iterable, Mapping


def dumps_risks(items: Iterable[Mapping[str, object]]) -> str:
    return json.dumps(list(items), sort_keys=True)

