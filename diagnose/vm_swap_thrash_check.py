#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Sample swap in/out rates to flag memory thrashing."""

import json
import time as t

SAMPLE_SECONDS = 1.0
WARN_PAGES_PER_SECOND = 500


def _vmstat():
    values = {}
    try:
        with open("/proc/vmstat", "r", encoding="utf-8") as handle:
            for line in handle:
                fields = line.split()
                if len(fields) == 2 and fields[1].isdigit():
                    values[fields[0]] = int(fields[1])
    except OSError:
        return {}
    return values


def diagnose():
    before = _vmstat()
    t.sleep(SAMPLE_SECONDS)
    after = _vmstat()
    swap_in = after.get("pswpin", 0) - before.get("pswpin", 0)
    swap_out = after.get("pswpout", 0) - before.get("pswpout", 0)
    rate_in = swap_in / SAMPLE_SECONDS
    rate_out = swap_out / SAMPLE_SECONDS
    findings = []
    if max(rate_in, rate_out) > WARN_PAGES_PER_SECOND:
        findings.append(
            {
                "severity": "warning",
                "detail": "swap rate in={:.0f}/s out={:.0f}/s".format(rate_in, rate_out),
            }
        )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "swap_thrash",
        "window_seconds": SAMPLE_SECONDS,
        "swap_in_per_second": round(rate_in, 2),
        "swap_out_per_second": round(rate_out, 2),
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
