#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Blend success rate and latency into a single collector health score."""

import logging

LOG = logging.getLogger(__name__)


def health_score(successes, attempts, latency_ms, target_ms=500.0):
    """Return a 0-100 score weighting reliability above latency."""
    if attempts <= 0:
        return 0.0
    reliability = max(0.0, min(1.0, successes / float(attempts)))
    if target_ms <= 0:
        latency_penalty = 0.0
    else:
        latency_penalty = min(1.0, max(0.0, latency_ms) / target_ms)
    score = 100.0 * (0.7 * reliability + 0.3 * (1.0 - latency_penalty))
    return round(score, 2)


def grade(score):
    """Bucket a numeric score into an operator facing label."""
    if score >= 90:
        return "healthy"
    if score >= 70:
        return "degraded"
    if score >= 40:
        return "unstable"
    return "failing"


class HealthTracker:
    """Accumulate attempts and produce scores on demand."""

    def __init__(self, target_ms=500.0):
        self.target_ms = float(target_ms)
        self.successes = 0
        self.attempts = 0
        self.latency_total = 0.0

    def observe(self, ok, latency_ms):
        """Record one attempt and return the updated score."""
        self.attempts += 1
        self.latency_total += max(0.0, float(latency_ms))
        if ok:
            self.successes += 1
        return self.score()

    def score(self):
        """Current score based on the running averages."""
        mean = self.latency_total / self.attempts if self.attempts else 0.0
        return health_score(self.successes, self.attempts, mean, self.target_ms)

    def label(self):
        """Human readable grade for the current score."""
        return grade(self.score())
