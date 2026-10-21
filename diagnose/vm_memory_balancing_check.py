#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Check NUMA node memory balance from the kernel node meminfo."""

import glob
import json
import time as t

IMBALANCE_RATIO = 0.25


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return ""


def _node_stats():
    nodes = []
    for path in sorted(glob.glob("/sys/devices/system/node/node*/meminfo")):
        total = 0
        free = 0
        for line in _read(path).splitlines():
            fields = line.replace(":", " ").split()
            if len(fields) < 4:
                continue
            if fields[2] == "MemTotal":
                total = int(fields[3])
            elif fields[2] == "MemFree":
                free = int(fields[3])
        nodes.append(
            {
                "node": path.split("/")[-2],
                "total_kb": total,
                "free_kb": free,
                "free_ratio": round(free / float(total), 4) if total else 0.0,
            }
        )
    return nodes


def diagnose():
    nodes = _node_stats()
    findings = []
    if len(nodes) > 1:
        ratios = [node["free_ratio"] for node in nodes]
        spread = max(ratios) - min(ratios)
        if spread > IMBALANCE_RATIO:
            findings.append(
                {
                    "severity": "warning",
                    "detail": "free memory ratio spread {:.2f} across numa nodes".format(
                        spread
                    ),
                }
            )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "memory_balancing",
        "nodes": nodes,
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
