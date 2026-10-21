#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Compare kernel uptime against the monotonic clock to spot drift."""

import json
import time as t

WARN_DRIFT_SECONDS = 2.0


def _uptime():
    try:
        with open("/proc/uptime", "r", encoding="utf-8") as handle:
            return float(handle.read().split()[0])
    except (OSError, ValueError, IndexError):
        return 0.0


def _clocksource():
    try:
        with open(
            "/sys/devices/system/clocksource/clocksource0/current_clocksource",
            "r",
            encoding="utf-8",
        ) as handle:
            return handle.read().strip()
    except OSError:
        return "unknown"


def diagnose():
    uptime = _uptime()
    monotonic = t.monotonic()
    drift = abs(uptime - monotonic)
    findings = []
    if drift > WARN_DRIFT_SECONDS:
        findings.append(
            {
                "severity": "warning",
                "detail": "uptime and monotonic differ by {:.2f}s".format(drift),
            }
        )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "clock_drift",
        "uptime_seconds": round(uptime, 3),
        "monotonic_seconds": round(monotonic, 3),
        "drift_seconds": round(drift, 3),
        "clocksource": _clocksource(),
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
