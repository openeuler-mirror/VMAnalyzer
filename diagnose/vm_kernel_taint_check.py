#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Decode kernel taint flags that point at out-of-tree drivers."""

import json
import time as t

FLAGS = (
    "proprietary_module",
    "forced_module_load",
    "unsupported_cpu",
    "forced_unload",
    "machine_check",
    "bad_page",
    "user_requested",
    "die",
    "oops",
    "acpi_overridden",
    "warning",
)


def _tainted():
    try:
        with open("/proc/sys/kernel/tainted", "r", encoding="utf-8") as handle:
            return int(handle.read().strip())
    except (OSError, ValueError):
        return 0


def diagnose():
    value = _tainted()
    active = [
        flag for bit, flag in enumerate(FLAGS) if value & (1 << bit)
    ]
    findings = [
        {"severity": "warning", "flag": flag, "detail": "kernel tainted: " + flag}
        for flag in active
    ]
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "kernel_taint",
        "tainted": value,
        "flags": active,
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
