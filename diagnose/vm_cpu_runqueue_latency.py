#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Diagnose CPU run queue latency from host pressure and load."""

import json
import os
import time as t

WARN_LOAD_PER_CPU = 2.0


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return ""


def _load():
    fields = _read("/proc/loadavg").split()
    if len(fields) < 3:
        return [0.0, 0.0, 0.0]
    try:
        return [float(value) for value in fields[:3]]
    except ValueError:
        return [0.0, 0.0, 0.0]


def _psi():
    for line in _read("/proc/pressure/cpu").splitlines():
        if not line.startswith("some"):
            continue
        for part in line.split()[1:]:
            key, _, value = part.partition("=")
            if key == "avg10":
                try:
                    return float(value)
                except ValueError:
                    return 0.0
    return 0.0


def diagnose():
    cpus = os.cpu_count() or 1
    load1, load5, load15 = _load()
    pressure = _psi()
    per_cpu = load1 / cpus
    findings = []
    if per_cpu > WARN_LOAD_PER_CPU:
        findings.append(
            {
                "severity": "warning",
                "detail": "load {:.2f} exceeds {:.2f} per cpu".format(
                    per_cpu, WARN_LOAD_PER_CPU
                ),
            }
        )
    if pressure > 20.0:
        findings.append(
            {"severity": "warning", "detail": "cpu pressure avg10 {:.1f}%".format(pressure)}
        )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "cpu_runqueue_latency",
        "cpus": cpus,
        "load": [load1, load5, load15],
        "load_per_cpu": round(per_cpu, 3),
        "pressure_avg10": pressure,
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
