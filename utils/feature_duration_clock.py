"""Monotonic duration clock helpers."""

from __future__ import annotations

import time


def now_seconds() -> float:
    return time.perf_counter()


def elapsed_seconds(start_seconds: float) -> float:
    return max(0.0, time.perf_counter() - start_seconds)

