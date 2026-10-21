#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Warn when the kernel entropy pool runs too low for guest crypto."""

import json
import time as t

MIN_ENTROPY_BITS = 128


def _read_int(path, default=0):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return int(handle.read().strip())
    except (OSError, ValueError):
        return default


def diagnose():
    available = _read_int("/proc/sys/kernel/random/entropy_avail")
    pool_size = _read_int("/proc/sys/kernel/random/poolsize", 4096)
    ratio = available / float(pool_size) if pool_size else 0.0
    findings = []
    if available < MIN_ENTROPY_BITS:
        findings.append(
            {
                "severity": "warning",
                "detail": "only {} bits of entropy available".format(available),
            }
        )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "entropy_pool",
        "entropy_avail": available,
        "pool_size": pool_size,
        "fill_ratio": round(ratio, 4),
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
