"""Risk helper import smoke test."""

from __future__ import annotations

import pytest


def test_risk_builder_importable():
    module = pytest.importorskip("utils.feature_risk_tag_builder")
    assert module.build_risk_tags({"cpu_usage": 90.0}) == ["high_cpu"]

