#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Measure the host context switch rate over a short window."""

import json
import os
import time as t

SAMPLE_SECONDS = 1.0
WARN_PER_CPU_PER_SECOND = 5000


def _ctxt():
    try:
        with open("/proc/stat", "r", encoding="utf-8") as handle:
            for line in handle:
                if line.startswith("ctxt "):
                    return int(line.split()[1])
    except (OSError, ValueError, IndexError):
        return 0
    return 0


def diagnose():
    cpus = os.cpu_count() or 1
    before = _ctxt()
    t.sleep(SAMPLE_SECONDS)
    after = _ctxt()
    switches = max(0, after - before)
    rate = switches / SAMPLE_SECONDS
    per_cpu = rate / cpus
    findings = []
    if per_cpu > WARN_PER_CPU_PER_SECOND:
        findings.append(
            {
                "severity": "warning",
                "detail": "context switches {:.0f}/s per cpu".format(per_cpu),
            }
        )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "context_switch_storm",
        "cpus": cpus,
        "switches_per_second": round(rate, 2),
        "per_cpu_per_second": round(per_cpu, 2),
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
