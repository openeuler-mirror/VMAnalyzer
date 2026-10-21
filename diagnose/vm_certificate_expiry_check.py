#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Scan certificate files and report ones nearing expiry."""

import glob
import json
import subprocess as sp
import time as t

CERT_DIR = "/etc/pki"
PATTERNS = ("*.pem", "*.crt")
WARN_SECONDS = 30 * 24 * 3600


def _expiring(path):
    try:
        completed = sp.run(
            ["openssl", "x509", "-in", path, "-noout", "-checkend", str(WARN_SECONDS)],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, sp.SubprocessError):
        return None
    if completed.returncode == 0:
        return False
    if completed.returncode == 1:
        return True
    return None


def diagnose():
    certificates = []
    findings = []
    for pattern in PATTERNS:
        for path in glob.glob("{}/**/{}".format(CERT_DIR, pattern), recursive=True):
            expiring = _expiring(path)
            if expiring is None:
                continue
            certificates.append({"path": path, "expiring": expiring})
            if expiring:
                findings.append(
                    {
                        "severity": "warning",
                        "path": path,
                        "detail": "certificate expires within 30 days",
                    }
                )
    report = {
        "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
        "check": "certificate_expiry",
        "directory": CERT_DIR,
        "checked": len(certificates),
        "certificates": certificates,
        "findings": findings,
        "status": "warning" if findings else "ok",
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    diagnose()
