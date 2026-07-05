"""Error report example."""

from __future__ import annotations

import json


def example_report() -> str:
    return json.dumps([{"type": "qga_failed", "message": "guest agent unavailable"}], sort_keys=True)

