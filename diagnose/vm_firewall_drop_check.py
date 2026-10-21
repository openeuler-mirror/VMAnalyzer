#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Count firewall DROP verdicts that may starve guest traffic."""

import json
import re
import subprocess as sp
import time as t

DROP = re.compile(r"^\s*(\d+)\s+\d+\s+DROP", re.MULTILINE)
NUMBER = re.compile(r"^\s*\[(\d+):(\d+)\]", re.MULTILINE)


def _iptables():
    try:
        completed = sp.run(
            "iptables -L -n -v", shell=True, capture_output=True, text=True, timeout=10
        )
        return completed.stdout
    except (OSError, sp.SubprocessError):
        return ""


def _nftables():
    try:
        completed = sp.run(
            "nft list ruleset", shell=True, capture_output=True, text=True, timeout=10
        )
        return completed.stdout
    except (OSError, sp.SubprocessError):
        return ""


def diagnose():
    tables = {
        "iptables": {
            "packets": sum(int(match.group(1)) for match in DROP.finditer(_iptables()))
        },
        "nftables": {
            "packets": sum(int(match.group(1)) for match in NUMBER.finditer(_nftables()))
        },
    }
    findings = [
        {
            "severity": "info",
            "table": name,
            "detail": "{} packets dropped".format(data["packets"]),
        }
        for name, data in tables.items()
        if data["packets"] > 0
    ]
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "firewall_drop",
        "tables": tables,
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
