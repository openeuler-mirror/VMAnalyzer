#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Compare NUMA hit and miss counters to detect placement imbalance."""

import json
import time as t

WARN_MISS_RATIO = 0.15


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read().strip()
    except OSError:
        return ""


def _stats():
    values = {}
    for line in _read("/sys/devices/system/node/node0/numastat").splitlines():
        fields = line.split()
        if len(fields) == 2 and fields[1].isdigit():
            values[fields[0]] = int(fields[1])
    return values


def diagnose():
    stats = _stats()
    hits = stats.get("numa_hit", 0)
    misses = stats.get("numa_miss", 0) + stats.get("numa_foreign", 0)
    total = hits + misses
    ratio = misses / float(total) if total else 0.0
    findings = []
    if total and ratio > WARN_MISS_RATIO:
        findings.append(
            {
                "severity": "warning",
                "detail": "numa miss ratio {:.1%}".format(ratio),
            }
        )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "numa_imbalance",
        "numa_hit": hits,
        "numa_miss": misses,
        "miss_ratio": round(ratio, 4),
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
