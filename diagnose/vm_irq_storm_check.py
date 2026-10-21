#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Detect interrupt storms where one IRQ line dominates activity."""

import json
import time as t

DOMINANT_SHARE = 0.6


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return ""


def _interrupts():
    rows = []
    for line in _read("/proc/interrupts").splitlines():
        fields = line.split()
        if not fields or not fields[0].endswith(":"):
            continue
        counts = []
        for value in fields[1:]:
            if not value.isdigit():
                break
            counts.append(int(value))
        if not counts:
            continue
        label = fields[len(counts) + 1] if len(fields) > len(counts) + 1 else fields[0]
        rows.append({"irq": fields[0].rstrip(":"), "label": label, "count": sum(counts)})
    return rows


def diagnose():
    rows = _interrupts()
    total = sum(row["count"] for row in rows)
    rows.sort(key=lambda row: row["count"], reverse=True)
    findings = []
    if total and rows:
        share = rows[0]["count"] / float(total)
        if share > DOMINANT_SHARE:
            findings.append(
                {
                    "severity": "warning",
                    "irq": rows[0]["irq"],
                    "detail": "single irq holds {:.1%} of interrupts".format(share),
                }
            )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "irq_storm",
        "total": total,
        "top": rows[:5],
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
