#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Count snapshots per domain and check free space for snapshot growth."""

import json
import shutil
import subprocess as sp
import time as t

SNAPSHOT_WARN = 8
FREE_WARN_RATIO = 0.10
POOL_PATH = "/var/lib/libvirt/images"


def _snapshot_names(domain):
    completed = sp.run(
        "virsh snapshot-list --name {}".format(domain),
        shell=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def _domains():
    completed = sp.run(
        "virsh list --all --name", shell=True, capture_output=True, text=True
    )
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def diagnose():
    domains = []
    findings = []
    for domain in _domains():
        names = _snapshot_names(domain)
        domains.append({"domain": domain, "snapshots": len(names)})
        if len(names) > SNAPSHOT_WARN:
            findings.append(
                {
                    "severity": "warning",
                    "domain": domain,
                    "detail": "{} snapshots retained".format(len(names)),
                }
            )
    free_ratio = 1.0
    try:
        usage = shutil.disk_usage(POOL_PATH)
        free_ratio = usage.free / float(usage.total) if usage.total else 0.0
    except OSError:
        pass
    if free_ratio < FREE_WARN_RATIO:
        findings.append(
            {
                "severity": "warning",
                "detail": "pool free space at {:.1%}".format(free_ratio),
            }
        )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "snapshot_space",
        "pool": POOL_PATH,
        "free_ratio": round(free_ratio, 4),
        "domains": domains,
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
