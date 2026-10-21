#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Report zswap configuration and compressed pool usage."""

import glob
import json
import time as t


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read().strip()
    except OSError:
        return ""


def _param(name):
    return _read("/sys/module/zswap/parameters/{}".format(name))


def _pool_stats():
    stats = {}
    for path in glob.glob("/sys/kernel/debug/zswap/*"):
        key = path.rsplit("/", 1)[-1]
        value = _read(path)
        if value.isdigit():
            stats[key] = int(value)
    return stats


def diagnose():
    enabled = _param("enabled")
    stats = _pool_stats()
    stored = stats.get("stored_pages", 0)
    pool = stats.get("pool_total_size", 0)
    findings = []
    if enabled in ("Y", "1", "y") and not stats:
        findings.append(
            {
                "severity": "info",
                "detail": "zswap enabled but debug stats are unavailable",
            }
        )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "zswap_usage",
        "enabled": enabled or "unknown",
        "compressor": _param("compressor"),
        "max_pool_percent": _param("max_pool_percent"),
        "stored_pages": stored,
        "pool_total_size": pool,
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
