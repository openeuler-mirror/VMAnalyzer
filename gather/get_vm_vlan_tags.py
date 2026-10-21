#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""List 802.1Q VLAN interfaces and their parent devices."""

import json
import time as t


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return ""


vlans = []
for line in _read("/proc/net/vlan/config").splitlines():
    fields = line.split()
    if len(fields) < 3 or fields[0].endswith("|"):
        continue
    if "|" not in line:
        continue
    name, _, rest = line.partition("|")
    vlan_id, _, parent = rest.strip().partition("|")
    vlans.append(
        {
            "name": name.strip(),
            "vlan_id": vlan_id.strip(),
            "parent": parent.strip(),
            "flags": fields[3:] if len(fields) > 3 else [],
        }
    )
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "vlan_count": len(vlans),
    "vlans": vlans,
}
print(json.dumps(report, indent=2))
