#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Map bridge interfaces to their member ports for network topology."""

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


bridges = {}
for path in sorted(glob.glob("/sys/class/net/*/bridge")):
    name = os.path.basename(os.path.dirname(path))
    ports = []
    for port in sorted(glob.glob("/sys/class/net/{}/brif/*".format(name))):
        ports.append(os.path.basename(port))
    bridges[name] = {
        "ports": ports,
        "port_count": len(ports),
        "stp_state": _read("/sys/class/net/{}/bridge/stp_state".format(name)),
        "forward_delay": _read("/sys/class/net/{}/bridge/forward_delay".format(name)),
    }
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "bridge_count": len(bridges),
    "bridges": bridges,
}
print(json.dumps(report, indent=2))
