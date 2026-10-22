#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Record entropy pool capacity and current availability."""

import json
import time as t


def _read_int(path, default=0):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return int(handle.read().strip())
    except (OSError, ValueError):
        return default


available = _read_int("/proc/sys/kernel/random/entropy_avail")
pool_size = _read_int("/proc/sys/kernel/random/poolsize")
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "entropy_avail": available,
    "pool_size": pool_size,
    "fill_ratio": round(available / float(pool_size), 4) if pool_size else 0.0,
    "write_wakeup_threshold": _read_int(
        "/proc/sys/kernel/random/write_wakeup_threshold"
    ),
    "urandom_min_reseed_secs": _read_int(
        "/proc/sys/kernel/random/urandom_min_reseed_secs"
    ),
}
print(json.dumps(report, indent=2))
