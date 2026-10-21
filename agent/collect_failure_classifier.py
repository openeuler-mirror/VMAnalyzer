#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Classify collection failures so retries can be targeted."""

import logging

LOG = logging.getLogger(__name__)

PATTERNS = (
    ("timeout", ("timeout", "timed out", "deadline")),
    ("agent_unavailable", ("agent", "qga", "channel")),
    ("permission", ("permission", "denied", "not authorized")),
    ("not_found", ("no such", "not found", "missing")),
    ("storage", ("disk", "i/o error", "enospc")),
)


def classify(message):
    """Return a coarse failure category for a log or exception message."""
    text = (message or "").lower()
    for category, needles in PATTERNS:
        if any(needle in text for needle in needles):
            return category
    return "unknown"


def retryable(category):
    """Whether a failure category is worth retrying immediately."""
    return category in ("timeout", "agent_unavailable", "storage")


def summarise(messages):
    """Count failures by category."""
    counts = {}
    for message in messages:
        category = classify(message)
        counts[category] = counts.get(category, 0) + 1
    LOG.debug("classified %d failures", len(messages))
    return counts
