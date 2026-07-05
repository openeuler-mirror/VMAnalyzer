"""Error JSON export helper."""

from __future__ import annotations

import json
from typing import Iterable, Mapping


def dumps_errors(errors: Iterable[Mapping[str, object]]) -> str:
    return json.dumps(list(errors), sort_keys=True)

