#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Count SSH authorized keys per account for access audits."""

import glob
import json
import os
import time as t


def _keys(path):
    entries = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                text = line.strip()
                if text and not text.startswith("#"):
                    entries.append(" ".join(text.split()[:2]))
    except OSError:
        return entries
    return entries


accounts = {}
paths = ["/root/.ssh/authorized_keys"]
paths.extend(sorted(glob.glob("/home/*/.ssh/authorized_keys")))
for path in paths:
    if not os.path.exists(path):
        continue
    keys = _keys(path)
    accounts[path] = {"count": len(keys), "types": sorted({key.split()[0] for key in keys})}
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "account_count": len(accounts),
    "key_count": sum(item["count"] for item in accounts.values()),
    "accounts": accounts,
}
print(json.dumps(report, indent=2))
