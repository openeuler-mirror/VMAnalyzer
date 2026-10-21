#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Collect per-mount options to spot missing noatime or unsafe flags."""

import json
import time as t

SKIP = ("/proc", "/sys", "/dev", "/run", "/snap")


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return ""


mounts = []
for line in _read("/proc/mounts").splitlines():
    fields = line.split()
    if len(fields) < 4 or fields[1].startswith(SKIP):
        continue
    options = fields[3].split(",")
    mounts.append(
        {
            "device": fields[0],
            "mountpoint": fields[1],
            "fstype": fields[2],
            "options": options,
            "noatime": "noatime" in options or "relatime" in options,
            "read_only": "ro" in options,
        }
    )
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "mount_count": len(mounts),
    "without_noatime": [item["mountpoint"] for item in mounts if not item["noatime"]],
    "mounts": mounts,
}
print(json.dumps(report, indent=2))
