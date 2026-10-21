#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Collect configured DNS servers and resolver options for guests."""

import json
import time as t


def _lines(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.readlines()
    except OSError:
        return []


servers = []
search = []
options = []
for line in _lines("/etc/resolv.conf"):
    text = line.strip()
    if not text or text.startswith(("#", ";")):
        continue
    fields = text.split()
    if len(fields) < 2:
        continue
    if fields[0] == "nameserver":
        servers.append(fields[1])
    elif fields[0] == "search":
        search.extend(fields[1:])
    elif fields[0] == "options":
        options.extend(fields[1:])
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "server_count": len(servers),
    "servers": servers,
    "search_domains": search,
    "options": options,
}
print(json.dumps(report, indent=2))
