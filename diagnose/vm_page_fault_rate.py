#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Sample page fault rates to catch memory overcommit pressure."""

import json
import time as t

SAMPLE_SECONDS = 1.0
WARN_MAJOR_PER_SECOND = 100


def _vmstat():
    values = {}
    try:
        with open("/proc/vmstat", "r", encoding="utf-8") as handle:
            for line in handle:
                fields = line.split()
                if len(fields) == 2 and fields[1].isdigit():
                    values[fields[0]] = int(fields[1])
    except OSError:
        return values
    return values


def diagnose():
    before = _vmstat()
    t.sleep(SAMPLE_SECONDS)
    after = _vmstat()
    minor = after.get("pgfault", 0) - before.get("pgfault", 0)
    major = after.get("pgmajfault", 0) - before.get("pgmajfault", 0)
    rate = major / SAMPLE_SECONDS
    findings = []
    if rate > WARN_MAJOR_PER_SECOND:
        findings.append(
            {
                "severity": "warning",
                "detail": "major faults at {:.0f}/s".format(rate),
            }
        )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "page_fault_rate",
        "window_seconds": SAMPLE_SECONDS,
        "minor_faults": minor,
        "major_faults": major,
        "major_per_second": round(rate, 2),
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
