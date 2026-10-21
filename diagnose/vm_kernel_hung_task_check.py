#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Look for hung task warnings in the kernel ring buffer."""

import json
import re
import subprocess as sp
import time as t

HUNG = re.compile(r"blocked for more than (\d+) seconds", re.IGNORECASE)


def _dmesg():
    try:
        completed = sp.run(
            "dmesg --ctime", shell=True, capture_output=True, text=True, timeout=10
        )
        return completed.stdout
    except (OSError, sp.SubprocessError):
        return ""


def _sysctl_hung_timeout():
    try:
        with open("/proc/sys/kernel/hung_task_timeout_secs") as handle:
            return int(handle.read().strip())
    except (OSError, ValueError):
        return 120


def diagnose():
    lines = _dmesg().splitlines()
    hits = []
    for line in lines:
        match = HUNG.search(line)
        if match:
            hits.append(
                {
                    "seconds": int(match.group(1)),
                    "message": line.strip()[:240],
                }
            )
    findings = [
        {
            "severity": "critical",
            "detail": "task blocked {}s".format(hit["seconds"]),
        }
        for hit in hits
    ]
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "kernel_hung_task",
        "timeout_secs": _sysctl_hung_timeout(),
        "hung_tasks": hits,
        "findings": findings,
        "status": "critical" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
