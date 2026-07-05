"""Duration helper import smoke test."""

from __future__ import annotations

import pytest


def test_duration_clock_importable():
    module = pytest.importorskip("utils.feature_duration_clock")
    assert module.now_seconds() >= 0.0

