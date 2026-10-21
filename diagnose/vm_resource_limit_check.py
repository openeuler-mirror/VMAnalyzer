#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Audit ulimits of running qemu processes for undersized limits."""

import glob
import json
import time as t

MIN_OPEN_FILES = 4096


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return ""


def _qemu_pids():
    pids = []
    for path in glob.glob("/proc/[0-9]*/comm"):
        if "qemu" in _read(path).strip().lower():
            pids.append(path.split("/")[2])
    return pids


def _open_limit(pid):
    for line in _read("/proc/{}/limits".format(pid)).splitlines():
        if line.startswith("Max open files"):
            fields = line.split()
            try:
                return int(fields[3])
            except (IndexError, ValueError):
                return None
    return None


def diagnose():
    processes = []
    findings = []
    for pid in _qemu_pids():
        soft = _open_limit(pid)
        command = _read("/proc/{}/cmdline".format(pid)).replace("\x00", " ").strip()
        processes.append({"pid": pid, "max_open_files": soft, "command": command[:120]})
        if soft is not None and soft < MIN_OPEN_FILES:
            findings.append(
                {
                    "severity": "warning",
                    "pid": pid,
                    "detail": "max open files limited to {}".format(soft),
                }
            )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "resource_limit",
        "qemu_processes": len(processes),
        "processes": processes,
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
