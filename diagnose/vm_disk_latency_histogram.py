#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Build a latency histogram from /proc/diskstats service counters."""

import json
import time as t

BUCKETS = (1, 5, 10, 20, 50, 100, 500)
WARN_AWAIT_MS = 20.0


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return ""


def _samples():
    rows = []
    for line in _read("/proc/diskstats").splitlines():
        fields = line.split()
        if len(fields) < 14 or fields[2].startswith(("loop", "ram")):
            continue
        try:
            reads = int(fields[3])
            read_ms = int(fields[6])
            writes = int(fields[7])
            write_ms = int(fields[10])
        except ValueError:
            continue
        rows.append((fields[2], reads, read_ms, writes, write_ms))
    return rows


def _bucket(await_ms):
    for edge in BUCKETS:
        if await_ms <= edge:
            return "<=%dms" % edge
    return ">%dms" % BUCKETS[-1]


def diagnose():
    devices = []
    histogram = {}
    for name, reads, read_ms, writes, write_ms in _samples():
        ops = reads + writes
        if ops <= 0:
            continue
        await_ms = (read_ms + write_ms) / float(ops)
        label = _bucket(await_ms)
        histogram[label] = histogram.get(label, 0) + ops
        devices.append({"device": name, "await_ms": round(await_ms, 3), "ops": ops})
    devices.sort(key=lambda item: item["await_ms"], reverse=True)
    findings = [
        {
            "severity": "warning",
            "device": item["device"],
            "detail": "average await {:.1f}ms".format(item["await_ms"]),
        }
        for item in devices
        if item["await_ms"] > WARN_AWAIT_MS
    ]
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "disk_latency_histogram",
        "devices": devices,
        "histogram": histogram,
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
