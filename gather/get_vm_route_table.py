#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Capture default and gateway routes for guest reachability audits."""

import json
import subprocess as sp
import time as t


def _routes():
    try:
        completed = sp.run(
            "ip route show", shell=True, capture_output=True, text=True, timeout=10
        )
        return completed.stdout
    except (OSError, sp.SubprocessError):
        return ""


routes = []
defaults = []
for line in _routes().splitlines():
    fields = line.split()
    if not fields:
        continue
    entry = {
        "route": fields[0],
        "target": fields[1] if len(fields) > 2 else fields[0],
        "raw": line.strip(),
    }
    routes.append(entry)
    if fields[0] == "default":
        defaults.append(line.strip())
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "route_count": len(routes),
    "default_count": len(defaults),
    "defaults": defaults,
    "routes": routes,
}
print(json.dumps(report, indent=2))
