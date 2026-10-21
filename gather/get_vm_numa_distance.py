#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Collect NUMA node distance matrices used for placement scoring."""

import glob
import json
import os
import time as t


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read().strip()
    except OSError:
        return ""


nodes = {}
for path in sorted(glob.glob("/sys/devices/system/node/node*/distance")):
    node = os.path.basename(os.path.dirname(path))
    distances = [int(value) for value in _read(path).split() if value.isdigit()]
    nodes[node] = {
        "distances": distances,
        "local_distance": distances[int(node.replace("node", ""))]
        if len(distances) > int(node.replace("node", ""))
        else None,
    }
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "node_count": len(nodes),
    "nodes": nodes,
    "online": _read("/sys/devices/system/node/online"),
}
print(json.dumps(report, indent=2))
