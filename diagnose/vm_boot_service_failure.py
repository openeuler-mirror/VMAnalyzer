#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""List systemd units that failed during or after boot."""

import json
import subprocess as sp
import time as t


def _failed():
    try:
        completed = sp.run(
            "systemctl --failed --no-legend --plain",
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, sp.SubprocessError):
        return []
    units = []
    for line in completed.stdout.splitlines():
        fields = line.split()
        if len(fields) < 2:
            continue
        units.append({"unit": fields[0], "load": fields[1], "active": fields[2]})
    return units


def diagnose():
    units = _failed()
    findings = [
        {
            "severity": "warning",
            "unit": item["unit"],
            "detail": "unit in {} state".format(item["active"]),
        }
        for item in units
    ]
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "boot_service_failure",
        "failed_count": len(units),
        "units": units,
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
