#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Warn when the newest VM backup is older than the allowed age."""

import glob
import json
import os
import time as t

BACKUP_DIR = "/var/lib/libvirt/backups"
PATTERNS = ("*.qcow2", "*.img", "*.tar.gz", "*.xml")
MAX_AGE_HOURS = 48.0


def _newest(directory):
    newest = 0.0
    count = 0
    for pattern in PATTERNS:
        for path in glob.glob(os.path.join(directory, pattern)):
            try:
                stamp = os.path.getmtime(path)
            except OSError:
                continue
            newest = max(newest, stamp)
            count += 1
    return newest, count


def diagnose():
    newest, count = _newest(BACKUP_DIR)
    age_hours = (t.time() - newest) / 3600.0 if newest else None
    findings = []
    if count == 0:
        findings.append(
            {"severity": "warning", "detail": "no backups found in " + BACKUP_DIR}
        )
    elif age_hours is not None and age_hours > MAX_AGE_HOURS:
        findings.append(
            {
                "severity": "warning",
                "detail": "newest backup is {:.1f}h old".format(age_hours),
            }
        )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "backup_freshness",
        "directory": BACKUP_DIR,
        "backup_count": count,
        "age_hours": round(age_hours, 2) if age_hours is not None else None,
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
