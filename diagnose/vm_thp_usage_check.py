#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Measure transparent huge page coverage relative to total memory."""

import json
import time as t

LOW_COVERAGE = 0.10


def _meminfo():
    values = {}
    try:
        with open("/proc/meminfo", "r", encoding="utf-8") as handle:
            for line in handle:
                key, _, rest = line.partition(":")
                fields = rest.split()
                if fields:
                    values[key.strip()] = int(fields[0])
    except (OSError, ValueError):
        return {}
    return values


def diagnose():
    values = _meminfo()
    total = values.get("MemTotal", 0)
    anon_huge = values.get("AnonHugePages", 0)
    shmem_huge = values.get("ShmemHugePages", 0)
    huge_total = anon_huge + shmem_huge
    coverage = huge_total / float(total) if total else 0.0
    findings = []
    if total and coverage < LOW_COVERAGE:
        findings.append(
            {
                "severity": "info",
                "detail": "huge page coverage only {:.1%}".format(coverage),
            }
        )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "thp_usage",
        "mem_total_kb": total,
        "anon_huge_kb": anon_huge,
        "shmem_huge_kb": shmem_huge,
        "coverage": round(coverage, 4),
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
