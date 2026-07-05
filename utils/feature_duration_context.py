"""Duration context manager."""

from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Iterator, MutableMapping


@contextmanager
def duration_context(name: str) -> Iterator[MutableMapping[str, object]]:
    item: MutableMapping[str, object] = {"name": name}
    start = time.perf_counter()
    try:
        yield item
    finally:
        item["elapsed_seconds"] = time.perf_counter() - start

