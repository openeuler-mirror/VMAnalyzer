#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Snapshot sysctl values that influence virtualisation behaviour."""

import json
import time as t

KEYS = (
    "kernel.numa_balancing",
    "kernel.sched_autogroup_enabled",
    "vm.swappiness",
    "vm.dirty_ratio",
    "vm.dirty_background_ratio",
    "vm.overcommit_memory",
    "vm.zone_reclaim_mode",
    "net.core.somaxconn",
)


def _read(key):
    path = "/proc/sys/" + key.replace(".", "/")
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read().strip()
    except OSError:
        return None


values = {}
for key in KEYS:
    values[key] = _read(key)
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "available": sum(1 for value in values.values() if value is not None),
    "values": values,
}
print(json.dumps(report, indent=2))
