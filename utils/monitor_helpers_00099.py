#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Memory balloon pressure analysis helpers.

The virtio-balloon driver reports guest memory accounting such as free memory,
total memory and major page faults.  These helpers turn raw balloon samples
into utilization ratios and host-pressure hints so that VMs which are about to
start reclaiming memory can be ranked before they become unresponsive.
"""
import logging

LOG = logging.getLogger(__name__)


def _to_kib_00099(value):
    """Balloon counters are reported in KiB; coerce safely."""
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def parse_balloon_stats_00099(raw):
    """Normalize a raw balloon stats mapping into integer KiB counters."""
    keys = ("total", "free", "available", "swap_in", "swap_out",
            "major_fault", "minor_fault")
    stats = {key: _to_kib_00099(raw.get(key, 0)) for key in keys}
    stats["valid"] = stats["total"] > 0
    return stats


def memory_utilization_00099(stats):
    """Return used ratio, free ratio and pressure margin in percent."""
    if not stats.get("valid"):
        LOG.warning("invalid balloon stats, utilization undefined")
        return {"used_ratio": 0.0, "free_ratio": 0.0, "pressure_margin_pct": 100.0}
    total = float(stats["total"])
    reference = stats["available"] if stats["available"] else stats["free"]
    used_ratio = max(0.0, min(1.0, (total - reference) / total))
    free_ratio = max(0.0, min(1.0, reference / total))
    return {
        "used_ratio": round(used_ratio, 4),
        "free_ratio": round(free_ratio, 4),
        "used_pct": round(used_ratio * 100, 2),
        "pressure_margin_pct": round(free_ratio * 100, 2),
    }


def detect_reclaim_activity_00099(stats, fault_threshold=1000):
    """Detect active memory reclaim from swap and major-fault counters."""
    signals = []
    if stats.get("swap_in", 0) > 0 or stats.get("swap_out", 0) > 0:
        signals.append("swap")
    if stats.get("major_fault", 0) >= fault_threshold:
        signals.append("major_faults")
    return signals


def classify_pressure_00099(utilization, signals, warn_pct=85.0, crit_pct=95.0):
    """Classify guest memory pressure as healthy/warning/critical."""
    used = utilization.get("used_pct", 0.0)
    if used >= crit_pct or "swap" in signals:
        return "critical"
    if used >= warn_pct or "major_faults" in signals:
        return "warning"
    return "healthy"


def summarize_balloon_00099(raw, fault_threshold=1000):
    """Produce a compact pressure summary from one balloon sample."""
    stats = parse_balloon_stats_00099(raw)
    utilization = memory_utilization_00099(stats)
    signals = detect_reclaim_activity_00099(stats, fault_threshold)
    level = classify_pressure_00099(utilization, signals)
    return {
        "level": level,
        "signals": signals,
        "total_kib": stats["total"],
        "available_kib": stats["available"],
        "utilization": utilization,
    }


__all__ = [
    "parse_balloon_stats_00099",
    "memory_utilization_00099",
    "detect_reclaim_activity_00099",
    "classify_pressure_00099",
    "summarize_balloon_00099",
]
