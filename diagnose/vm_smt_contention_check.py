#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Map SMT sibling topology to guide vCPU pinning decisions."""

import glob
import json
import time as t


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read().strip()
    except OSError:
        return ""


def _siblings():
    cores = []
    for path in sorted(glob.glob("/sys/devices/system/cpu/cpu[0-9]*/topology")):
        cpu = path.split("/")[-2]
        siblings = _read(path + "/thread_siblings_list")
        core_id = _read(path + "/core_id")
        cores.append({"cpu": cpu, "core_id": core_id, "siblings": siblings})
    return cores


def diagnose():
    cores = _siblings()
    shared = {}
    for item in cores:
        siblings = item["siblings"]
        if siblings:
            shared.setdefault(siblings, []).append(item["cpu"])
    contended = [
        {"siblings": key, "cpus": value}
        for key, value in shared.items()
        if len(value) > 1
    ]
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "smt_contention",
        "cpu_count": len(cores),
        "sibling_groups": contended,
        "findings": [],
        "status": "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
