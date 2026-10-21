#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Check cpufreq governors because powersave hurts latency sensitive VMs."""

import glob
import json
import time as t

LATENCY_SAFE = ("performance", "schedutil")


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read().strip()
    except OSError:
        return ""


def _policies():
    rows = []
    for path in sorted(glob.glob("/sys/devices/system/cpu/cpufreq/policy*")):
        affected = _read(path + "/affected_cpus")
        rows.append(
            {
                "policy": path.rsplit("/", 1)[-1],
                "governor": _read(path + "/scaling_governor"),
                "cpus": affected,
                "max_khz": _read(path + "/scaling_max_freq"),
            }
        )
    return rows


def diagnose():
    policies = _policies()
    findings = [
        {
            "severity": "warning",
            "policy": item["policy"],
            "detail": "governor {} adds wakeup latency".format(item["governor"]),
        }
        for item in policies
        if item["governor"] and item["governor"] not in LATENCY_SAFE
    ]
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "cpu_governor",
        "policies": policies,
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
