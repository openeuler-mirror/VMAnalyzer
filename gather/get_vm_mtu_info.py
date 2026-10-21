#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Summarise interface MTUs to catch mismatched paths for guests."""

import glob
import json
import os
import time as t


def _read(path, default="0"):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read().strip()
    except OSError:
        return default


interfaces = {}
for path in sorted(glob.glob("/sys/class/net/*/mtu")):
    name = os.path.basename(os.path.dirname(path))
    interfaces[name] = {
        "mtu": int(_read(path)),
        "type": _read("/sys/class/net/{}/type".format(name)),
        "master": _read("/sys/class/net/{}/master".format(name)) or None,
    }
values = [item["mtu"] for item in interfaces.values()]
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "interface_count": len(interfaces),
    "mtu_min": min(values) if values else 0,
    "mtu_max": max(values) if values else 0,
    "mixed_mtu": len(set(values)) > 1,
    "interfaces": interfaces,
}
print(json.dumps(report, indent=2))
