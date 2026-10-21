#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Detect guest filesystems that unexpectedly became read-only."""

import json
import subprocess as sp
import time as t

SKIP_PREFIXES = ("/proc", "/sys", "/dev/pts", "/run")


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return ""


def _mounts():
    entries = []
    for line in _read("/proc/mounts").splitlines():
        fields = line.split()
        if len(fields) < 4:
            continue
        device, mountpoint, fstype, options = fields[:4]
        if mountpoint.startswith(SKIP_PREFIXES):
            continue
        if fstype in ("proc", "sysfs", "devtmpfs", "tmpfs", "cgroup2", "overlay"):
            continue
        entries.append(
            {
                "device": device,
                "mountpoint": mountpoint,
                "fstype": fstype,
                "read_only": "ro" in options.split(","),
            }
        )
    return entries


def _domains():
    out = sp.run(
        "virsh list --name", shell=True, capture_output=True, text=True
    ).stdout
    return [line.strip() for line in out.splitlines() if line.strip()]


def diagnose():
    entries = _mounts()
    findings = [
        {
            "severity": "critical",
            "mountpoint": entry["mountpoint"],
            "detail": "filesystem {} mounted read-only".format(entry["fstype"]),
        }
        for entry in entries
        if entry["read_only"]
    ]
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "guest_fs_readonly",
        "domains": _domains(),
        "mounts": entries,
        "findings": findings,
        "status": "critical" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
