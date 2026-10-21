#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Collect kernel release and build details for compatibility checks."""

import json
import os
import platform
import time as t


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read().strip()
    except OSError:
        return ""


uname = platform.uname()
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "release": uname.release,
    "version": _read("/proc/version"),
    "machine": uname.machine,
    "kernel_type": _read("/proc/sys/kernel/ostype"),
    "kernel_osrelease": _read("/proc/sys/kernel/osrelease"),
    "boot_time": _read("/proc/stat").split("btime")[-1].split()[0]
    if "btime" in _read("/proc/stat")
    else "",
    "boot_id": _read("/proc/sys/kernel/random/boot_id"),
    "cpu_count": os.cpu_count() or 0,
}
print(json.dumps(report, indent=2))
