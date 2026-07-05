"""Duration report example."""

from __future__ import annotations

import json


def example_report() -> str:
    return json.dumps([{"name": "cpu", "elapsed_seconds": 0.1, "status": "ok"}], sort_keys=True)

