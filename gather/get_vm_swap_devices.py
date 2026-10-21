#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""List swap devices with size and utilisation for capacity planning."""

import json
import time as t


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return ""


devices = []
for line in _read("/proc/swaps").splitlines()[1:]:
    fields = line.split()
    if len(fields) < 5:
        continue
    try:
        size_kb = int(fields[2])
        used_kb = int(fields[3])
    except ValueError:
        continue
    devices.append(
        {
            "device": fields[0],
            "type": fields[1],
            "size_kb": size_kb,
            "used_kb": used_kb,
            "used_ratio": round(used_kb / float(size_kb), 4) if size_kb else 0.0,
            "priority": fields[4],
        }
    )
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "swap_count": len(devices),
    "total_kb": sum(item["size_kb"] for item in devices),
    "used_kb": sum(item["used_kb"] for item in devices),
    "devices": devices,
}
print(json.dumps(report, indent=2))
