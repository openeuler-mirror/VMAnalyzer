"""Health helper import smoke test."""

from __future__ import annotations

import pytest


def test_health_calc_importable():
    module = pytest.importorskip("utils.feature_health_score_calc")
    assert module.calculate_health_score({}) == 100.0

