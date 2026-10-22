#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""List TCP listening ports exposed on the hypervisor host."""

import json
import subprocess as sp
import time as t


def _listeners():
    try:
        completed = sp.run(
            "ss -ltn", shell=True, capture_output=True, text=True, timeout=8
        )
        return completed.stdout
    except (OSError, sp.SubprocessError):
        return ""


listeners = []
for line in _listeners().splitlines():
    fields = line.split()
    if len(fields) < 4 or fields[0] == "State":
        continue
    address = fields[3]
    host, _, port = address.rpartition(":")
    listeners.append(
        {
            "address": host,
            "port": port,
            "local": host in ("127.0.0.1", "[::1]", "localhost"),
        }
    )
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "listener_count": len(listeners),
    "public_count": sum(1 for item in listeners if not item["local"]),
    "listeners": listeners,
}
print(json.dumps(report, indent=2))
