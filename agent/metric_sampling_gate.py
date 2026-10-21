#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Deterministic sampling for high-cardinality metric streams.

Hashing the series key keeps the keep/drop decision stable across cycles,
so dashboards do not flicker between sampled and unsampled points.
"""

import logging
import zlib

LOG = logging.getLogger(__name__)
SCALE = 1000


def series_key(vm_name, metric):
    """Stable key identifying one sampled series."""
    return "{}::{}".format(vm_name, metric)


def bucket_of(vm_name, metric, scale=SCALE):
    """Map a series key onto an integer bucket below *scale*."""
    digest = zlib.crc32(series_key(vm_name, metric).encode("utf-8"))
    return digest % scale


def should_sample(vm_name, metric, rate):
    """Keep the series when its bucket falls under the sampling rate."""
    if rate >= 1.0:
        return True
    if rate <= 0.0:
        return False
    return bucket_of(vm_name, metric) < int(rate * SCALE)


class SamplingGate:
    """Track how many series survived sampling for logging."""

    def __init__(self, rate):
        self.rate = max(0.0, min(1.0, float(rate)))
        self.kept = 0
        self.dropped = 0

    def admit(self, vm_name, metric):
        """Return True when the series should be collected this cycle."""
        if should_sample(vm_name, metric, self.rate):
            self.kept += 1
            return True
        self.dropped += 1
        LOG.debug("sampled out %s", series_key(vm_name, metric))
        return False

    def keep_ratio(self):
        """Fraction of admitted series so far."""
        total = self.kept + self.dropped
        return self.kept / float(total) if total else 0.0
