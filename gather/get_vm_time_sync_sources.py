#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Enumerate configured time sources for guest clock sync validation."""

import json
import subprocess as sp
import time as t


def _run(command):
    try:
        completed = sp.run(
            command, shell=True, capture_output=True, text=True, timeout=8
        )
        return completed.stdout
    except (OSError, sp.SubprocessError):
        return ""


def _chrony():
    peers = []
    for line in _run("chronyc sources -n").splitlines():
        fields = line.split()
        if len(fields) >= 3 and fields[0].startswith(("^", "=")):
            peers.append({"source": fields[1], "state": fields[2], "raw": line.strip()})
        elif len(fields) >= 2 and fields[0].startswith(("^", "=")):
            peers.append({"source": fields[1], "state": "", "raw": line.strip()})
    return peers


def _ntp():
    peers = []
    for line in _run("ntpq -pn").splitlines():
        fields = line.split()
        if fields and fields[0].startswith("*"):
            peers.append({"source": fields[0].lstrip("*"), "state": "sys.peer"})
    return peers


chrony = _chrony()
ntp = _ntp()
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "chrony_peers": chrony,
    "ntp_peers": ntp,
    "source_count": len(chrony) + len(ntp),
    "synchronized": _run("timedatectl show --property=NTPSynchronized --value").strip(),
}
print(json.dumps(report, indent=2))
