#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Audit per-disk cache modes for unsafe write caching settings."""

import json
import re
import subprocess as sp
import time as t

CACHE = re.compile(r"cache='?([a-z]+)'?")
UNSAFE = ("unsafe", "writeback")


def _xml(domain):
    completed = sp.run(
        "virsh dumpxml {}".format(domain), shell=True, capture_output=True, text=True
    )
    return completed.stdout


def _domains():
    completed = sp.run(
        "virsh list --name", shell=True, capture_output=True, text=True
    )
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def diagnose():
    disks = []
    findings = []
    for domain in _domains():
        for match in CACHE.finditer(_xml(domain)):
            mode = match.group(1)
            disks.append({"domain": domain, "cache": mode})
            if mode in UNSAFE:
                findings.append(
                    {
                        "severity": "warning",
                        "domain": domain,
                        "detail": "disk uses {} cache mode".format(mode),
                    }
                )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "disk_write_cache",
        "disks": disks,
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
