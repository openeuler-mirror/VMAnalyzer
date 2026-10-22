#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Read login policy limits applied to guest account passwords."""

import json
import time as t

KEYS = (
    "PASS_MAX_DAYS",
    "PASS_MIN_DAYS",
    "PASS_MIN_LEN",
    "PASS_WARN_AGE",
    "UMASK",
    "LOGIN_RETRIES",
)


def _login_defs():
    values = {}
    try:
        with open("/etc/login.defs", "r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                text = line.strip()
                if not text or text.startswith("#"):
                    continue
                fields = text.split()
                if len(fields) >= 2 and fields[0] in KEYS:
                    values[fields[0]] = fields[1]
    except OSError:
        pass
    return values


policy = _login_defs()
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "login_defs": policy,
    "missing": [key for key in KEYS if key not in policy],
}
print(json.dumps(report, indent=2))
