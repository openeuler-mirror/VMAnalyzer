#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Measure DNS resolution latency using the configured resolvers."""

import json
import socket
import time as t

WARN_MS = 200.0
PROBE_HOST = "localhost"


def _resolvers():
    servers = []
    try:
        with open("/etc/resolv.conf", "r", encoding="utf-8") as handle:
            for line in handle:
                fields = line.split()
                if len(fields) >= 2 and fields[0] == "nameserver":
                    servers.append(fields[1])
    except OSError:
        pass
    return servers


def _timed_lookup(host):
    start = t.perf_counter()
    try:
        socket.getaddrinfo(host, None)
        ok = True
    except socket.gaierror:
        ok = False
    return round((t.perf_counter() - start) * 1000.0, 3), ok


def diagnose():
    latency_ms, ok = _timed_lookup(PROBE_HOST)
    findings = []
    if not ok:
        findings.append({"severity": "warning", "detail": "localhost lookup failed"})
    elif latency_ms > WARN_MS:
        findings.append(
            {
                "severity": "warning",
                "detail": "lookup took {:.1f}ms".format(latency_ms),
            }
        )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "dns_latency",
        "resolvers": _resolvers(),
        "latency_ms": latency_ms,
        "resolved": ok,
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
