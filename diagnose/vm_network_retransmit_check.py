#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Diagnose TCP retransmission ratio from /proc/net/snmp."""

import json
import time as t

WARN_RATIO = 0.02


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return ""


def _tcp_counters():
    header = None
    values = None
    for line in _read("/proc/net/snmp").splitlines():
        if line.startswith("Tcp:"):
            fields = line.split()[1:]
            if header is None:
                header = fields
            else:
                values = fields
    if not header or not values:
        return {}
    return {
        name: int(value)
        for name, value in zip(header, values)
        if value.isdigit()
    }


def diagnose():
    counters = _tcp_counters()
    segments = counters.get("OutSegs", 0)
    retrans = counters.get("RetransSegs", 0)
    ratio = retrans / float(segments) if segments else 0.0
    findings = []
    if ratio > WARN_RATIO:
        findings.append(
            {
                "severity": "warning",
                "detail": "retransmission ratio {:.2%} above {:.2%}".format(
                    ratio, WARN_RATIO
                ),
            }
        )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "network_retransmit",
        "out_segments": segments,
        "retrans_segments": retrans,
        "retrans_ratio": round(ratio, 6),
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
