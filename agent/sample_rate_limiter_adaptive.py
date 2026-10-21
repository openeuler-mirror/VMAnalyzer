#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Adaptive sampling rate driven by recent collection latency."""

import logging

LOG = logging.getLogger(__name__)


class AdaptiveSampler:
    """Raise the rate when fast, lower it when cycles run long."""

    def __init__(self, rate=1.0, target_ms=800.0, step=0.1, floor=0.1):
        self.rate = max(floor, min(1.0, rate))
        self.target_ms = float(target_ms)
        self.step = float(step)
        self.floor = float(floor)

    def observe(self, latency_ms):
        """Adjust the sampling rate after one collection cycle."""
        if latency_ms > self.target_ms:
            self.rate = max(self.floor, self.rate - self.step)
        elif latency_ms < self.target_ms * 0.5:
            self.rate = min(1.0, self.rate + self.step)
        LOG.debug("latency %.1fms adjusted rate to %.2f", latency_ms, self.rate)
        return self.rate

    def should_collect(self, counter):
        """Deterministic decision using the current rate and a counter."""
        if self.rate <= 0.0:
            return False
        period = max(1, int(round(1.0 / self.rate)))
        return counter % period == 0
