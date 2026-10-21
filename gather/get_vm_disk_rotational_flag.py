#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Record whether block devices are rotational to tune IO scheduling."""

import glob
import json
import os
import time as t


def _read(path, default=""):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read().strip()
    except OSError:
        return default


devices = []
for path in sorted(glob.glob("/sys/block/*/queue/rotational")):
    name = os.path.basename(os.path.dirname(os.path.dirname(path)))
    if name.startswith(("loop", "ram", "dm-", "md")):
        continue
    devices.append(
        {
            "device": name,
            "rotational": _read(path) == "1",
            "scheduler": _read("/sys/block/{}/queue/scheduler".format(name)),
            "logical_block_size": _read(
                "/sys/block/{}/queue/logical_block_size".format(name)
            ),
        }
    )
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "device_count": len(devices),
    "rotational_count": sum(1 for item in devices if item["rotational"]),
    "devices": devices,
}
print(json.dumps(report, indent=2))
