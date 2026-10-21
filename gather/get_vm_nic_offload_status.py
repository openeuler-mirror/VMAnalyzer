#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Collect hardware offload feature flags for host network devices."""

import glob
import json
import os
import subprocess as sp
import time as t


def _read(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read().strip()
    except OSError:
        return ""


def _features(name):
    try:
        completed = sp.run(
            ["ethtool", "-k", name], capture_output=True, text=True, timeout=5
        )
    except (OSError, sp.SubprocessError):
        return {}
    features = {}
    for line in completed.stdout.splitlines():
        key, separator, value = line.partition(":")
        if separator and value.strip() in ("on", "off"):
            features[key.strip()] = value.strip() == "on"
    return features


interfaces = {}
for path in sorted(glob.glob("/sys/class/net/*")):
    name = os.path.basename(path)
    if name == "lo":
        continue
    interfaces[name] = {
        "operstate": _read(path + "/operstate"),
        "mtu": _read(path + "/mtu"),
        "features": _features(name),
    }
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "interface_count": len(interfaces),
    "interfaces": interfaces,
}
print(json.dumps(report, indent=2))
