#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Rank per-CPU steal time to locate contended virtual CPUs."""

import json
import time as t

WARN_STEAL_PERCENT = 10.0


def _cpu_lines():
    try:
        with open("/proc/stat", "r", encoding="utf-8") as handle:
            return [line for line in handle if line.startswith("cpu")]
    except OSError:
        return []


def _steal(line):
    fields = line.split()
    if fields[0] == "cpu" or len(fields) < 9:
        return None
    values = []
    for value in fields[1:9]:
        try:
            values.append(int(value))
        except ValueError:
            return None
    total = sum(values)
    return values[7], total


def diagnose():
    cpus = []
    for line in _cpu_lines():
        parsed = _steal(line)
        if parsed is None:
            continue
        steal, total = parsed
        percent = 100.0 * steal / total if total else 0.0
        cpus.append(
            {"cpu": line.split()[0], "steal": steal, "percent": round(percent, 3)}
        )
    cpus.sort(key=lambda item: item["percent"], reverse=True)
    findings = [
        {
            "severity": "warning",
            "cpu": item["cpu"],
            "detail": "steal time {:.1f}%".format(item["percent"]),
        }
        for item in cpus
        if item["percent"] > WARN_STEAL_PERCENT
    ]
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "vcpu_steal_correlation",
        "hot_cpus": cpus[:5],
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
