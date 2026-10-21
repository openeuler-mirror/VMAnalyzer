#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Find leftover empty cgroups that were never cleaned up."""

import glob
import json
import os
import time as t

ROOTS = (
    "/sys/fs/cgroup/machine.slice",
    "/sys/fs/cgroup/system.slice",
)


def _empty(path):
    try:
        return not os.listdir(path)
    except OSError:
        return False


def _groups(root):
    groups = []
    for path in glob.glob(os.path.join(root, "*.scope")):
        if not os.path.isdir(path):
            continue
        groups.append(
            {
                "path": path,
                "empty": _empty(path),
                "procs": _proc_count(path),
            }
        )
    return groups


def _proc_count(path):
    try:
        with open(os.path.join(path, "cgroup.procs"), "r", encoding="utf-8") as handle:
            return len([line for line in handle if line.strip()])
    except OSError:
        return 0


def diagnose():
    groups = []
    for root in ROOTS:
        groups.extend(_groups(root))
    leftovers = [item for item in groups if item["empty"] and item["procs"] == 0]
    findings = [
        {
            "severity": "info",
            "path": item["path"],
            "detail": "empty cgroup left behind",
        }
        for item in leftovers[:20]
    ]
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "cgroup_leak",
        "group_count": len(groups),
        "empty_count": len(leftovers),
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
