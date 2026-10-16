#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Disk I/O latency analysis helpers.

This module collects block-device latency samples (milliseconds) reported by
guest agents and turns them into percentile based statistics so that slow I/O
events can be detected even when the average latency looks healthy.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def percentile_00077(sorted_samples, pct):
    """Return the pct-th percentile (0-100) with nearest-rank interpolation."""
    if not sorted_samples:
        return 0.0
    if pct <= 0:
        return float(sorted_samples[0])
    if pct >= 100:
        return float(sorted_samples[-1])
    rank = (pct / 100.0) * (len(sorted_samples) - 1)
    low = int(math.floor(rank))
    high = int(math.ceil(rank))
    if low == high:
        return float(sorted_samples[low])
    fraction = rank - low
    return sorted_samples[low] + (sorted_samples[high] - sorted_samples[low]) * fraction


def summarize_disk_latency_00077(samples):
    """Build a latency summary (min/max/mean/p50/p90/p95/p99/stddev)."""
    values = [float(s) for s in samples if isinstance(s, (int, float)) and s >= 0]
    if not values:
        LOG.warning("summarize_disk_latency_00077 received no usable samples")
        return {"sample_count": 0}

    ordered = sorted(values)
    total = sum(ordered)
    mean = total / len(ordered)
    variance = sum((v - mean) ** 2 for v in ordered) / len(ordered)
    return {
        "sample_count": len(ordered),
        "min_ms": round(ordered[0], 3),
        "max_ms": round(ordered[-1], 3),
        "mean_ms": round(mean, 3),
        "stddev_ms": round(math.sqrt(variance), 3),
        "p50_ms": round(percentile_00077(ordered, 50), 3),
        "p90_ms": round(percentile_00077(ordered, 90), 3),
        "p95_ms": round(percentile_00077(ordered, 95), 3),
        "p99_ms": round(percentile_00077(ordered, 99), 3),
    }


def evaluate_io_sla_00077(summary, warn_ms=20.0, fail_ms=50.0):
    """Classify a latency summary against warn/fail SLA thresholds."""
    if summary.get("sample_count", 0) == 0:
        return "unknown"
    if summary["p99_ms"] >= fail_ms or summary["max_ms"] >= fail_ms * 2:
        return "critical"
    if summary["p95_ms"] >= warn_ms or summary["mean_ms"] >= warn_ms:
        return "degraded"
    return "healthy"


def parse_iostat_lines_00077(lines, device_filter=None):
    """Parse 'device await_ms' lines into {device: [latency samples]}."""
    result = {}
    for line in lines or []:
        parts = str(line).split()
        if len(parts) < 2:
            continue
        device, await_ms = parts[0], parts[-1]
        if device_filter and device not in device_filter:
            continue
        try:
            result.setdefault(device, []).append(float(await_ms))
        except ValueError:
            LOG.debug("skip non-numeric latency sample for %s: %r", device, await_ms)
    return result


__all__ = [
    "percentile_00077",
    "summarize_disk_latency_00077",
    "evaluate_io_sla_00077",
    "parse_iostat_lines_00077",
]
