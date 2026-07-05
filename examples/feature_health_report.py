"""Health report example."""

from __future__ import annotations

import json


def example_report() -> str:
    return json.dumps([{"vm": "demo", "health_score": 92.0}], sort_keys=True)

