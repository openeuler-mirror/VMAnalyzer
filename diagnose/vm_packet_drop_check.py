#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Report per-interface packet drops from /proc/net/dev."""

import json
import time as t

DROP_RATIO = 0.01


def _interfaces():
    rows = []
    try:
        with open("/proc/net/dev", "r", encoding="utf-8") as handle:
            lines = handle.readlines()[2:]
    except OSError:
        return rows
    for line in lines:
        name, _, data = line.partition(":")
        fields = data.split()
        if len(fields) < 16:
            continue
        try:
            rx_packets = int(fields[1])
            rx_drops = int(fields[2])
            tx_packets = int(fields[8])
            tx_drops = int(fields[9])
        except ValueError:
            continue
        rows.append(
            {
                "interface": name.strip(),
                "rx_packets": rx_packets,
                "rx_drops": rx_drops,
                "tx_packets": tx_packets,
                "tx_drops": tx_drops,
            }
        )
    return rows


def diagnose():
    interfaces = _interfaces()
    findings = []
    for item in interfaces:
        packets = item["rx_packets"] + item["tx_packets"]
        drops = item["rx_drops"] + item["tx_drops"]
        item["drop_ratio"] = round(drops / float(packets), 6) if packets else 0.0
        if item["drop_ratio"] > DROP_RATIO:
            findings.append(
                {
                    "severity": "warning",
                    "interface": item["interface"],
                    "detail": "drop ratio {:.2%}".format(item["drop_ratio"]),
                }
            )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "packet_drop",
        "interfaces": interfaces,
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
