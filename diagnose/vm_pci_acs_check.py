#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Verify IOMMU grouping and ACS support for passthrough safety."""

import glob
import json
import time as t


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read().strip()
    except OSError:
        return ""


def _groups():
    groups = {}
    for path in glob.glob("/sys/kernel/iommu_groups/*/devices/*"):
        parts = path.split("/")
        group = parts[4]
        groups.setdefault(group, []).append(parts[-1])
    return groups


def diagnose():
    groups = _groups()
    shared = {key: value for key, value in groups.items() if len(value) > 1}
    acs = {
        "pcie_acs_override": "pcie_acs_override" in _read("/proc/cmdline"),
        "iommu_enabled": "iommu" in _read("/proc/cmdline"),
    }
    findings = [
        {
            "severity": "warning",
            "group": key,
            "detail": "{} devices share one iommu group".format(len(value)),
        }
        for key, value in shared.items()
    ]
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "pci_acs",
        "group_count": len(groups),
        "groups": groups,
        "boot_flags": acs,
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
