#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Read SELinux enforcing state together with policy configuration."""

import json
import os
import time as t


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read().strip()
    except OSError:
        return ""


def _config():
    values = {}
    for line in _read("/etc/selinux/config").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip()
    return values


enforce = _read("/sys/fs/selinux/enforce")
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "mounted": os.path.isdir("/sys/fs/selinux"),
    "enforce": {"0": "permissive", "1": "enforcing"}.get(enforce, "disabled"),
    "config": _config(),
    "policy_version": _read("/sys/fs/selinux/policyvers"),
    "deny_unknown": _read("/sys/fs/selinux/checkreqprot"),
}
print(json.dumps(report, indent=2))
