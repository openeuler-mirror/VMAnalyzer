"""Duration CSV export helper."""

from __future__ import annotations

import csv
import io
from typing import Iterable, Mapping


def dumps_duration_csv(items: Iterable[Mapping[str, object]]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["name", "elapsed_seconds", "status"])
    writer.writeheader()
    for item in items:
        writer.writerow({key: item.get(key, "") for key in writer.fieldnames})
    return output.getvalue()

