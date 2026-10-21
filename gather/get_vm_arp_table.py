#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Read the neighbour table to see which guests share a layer 2 path."""

import json
import time as t


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return ""


entries = []
for line in _read("/proc/net/arp").splitlines()[1:]:
    fields = line.split()
    if len(fields) < 6:
        continue
    complete = fields[2] != "0x0"
    entries.append(
        {
            "address": fields[0],
            "hw_type": fields[1],
            "flags": fields[2],
            "mac": fields[3],
            "device": fields[5],
            "complete": complete,
        }
    )
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "entry_count": len(entries),
    "incomplete_count": sum(1 for item in entries if not item["complete"]),
    "entries": entries,
}
print(json.dumps(report, indent=2))
