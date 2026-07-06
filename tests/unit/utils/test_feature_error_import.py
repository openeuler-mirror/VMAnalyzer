"""Error helper import smoke test."""

from __future__ import annotations

import pytest


def test_error_classifier_importable():
    module = pytest.importorskip("utils.feature_error_classifier")
    assert module.classify_error("timeout") == "command_timeout"

