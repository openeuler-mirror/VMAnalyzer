#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Collect IPv4 and IPv6 addresses with their interface and scope."""

import json
import subprocess as sp
import time as t


def _addr():
    try:
        completed = sp.run(
            "ip -o addr show", shell=True, capture_output=True, text=True, timeout=10
        )
        return completed.stdout
    except (OSError, sp.SubprocessError):
        return ""


addresses = []
for line in _addr().splitlines():
    fields = line.split()
    if len(fields) < 4:
        continue
    interface = fields[1].rstrip(":")
    family = fields[2]
    cidr = fields[3]
    scope = fields[5] if len(fields) > 5 else "global"
    addresses.append(
        {
            "interface": interface,
            "family": family,
            "address": cidr,
            "scope": scope,
        }
    )
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "address_count": len(addresses),
    "ipv4_count": sum(1 for item in addresses if item["family"] == "inet"),
    "addresses": addresses,
}
print(json.dumps(report, indent=2))
