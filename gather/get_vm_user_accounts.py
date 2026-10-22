#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""List interactive login accounts and their password state."""

import json
import time as t


def _passwd():
    try:
        with open("/etc/passwd", "r", encoding="utf-8", errors="replace") as handle:
            return handle.readlines()
    except OSError:
        return []


def _shadow_state():
    states = {}
    try:
        with open("/etc/shadow", "r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                fields = line.split(":")
                if len(fields) >= 2:
                    states[fields[0]] = "set" if fields[1] else "empty"
    except OSError:
        pass
    return states


shadow = _shadow_state()
users = []
for line in _passwd():
    fields = line.strip().split(":")
    if len(fields) < 7:
        continue
    try:
        uid = int(fields[2])
    except ValueError:
        continue
    if uid == 0 or uid >= 1000:
        users.append(
            {
                "name": fields[0],
                "uid": uid,
                "shell": fields[6],
                "password": shadow.get(fields[0], "unknown"),
            }
        )
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "account_count": len(users),
    "users": users,
}
print(json.dumps(report, indent=2))
