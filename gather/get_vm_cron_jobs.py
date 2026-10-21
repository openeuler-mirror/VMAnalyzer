#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Inventory cron entries that may collide with collection cycles."""

import glob
import json
import os
import time as t


def _jobs(path):
    entries = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                text = line.strip()
                if text and not text.startswith("#") and "=" not in text:
                    entries.append(text[:160])
    except OSError:
        return entries
    return entries


sources = {}
for path in sorted(glob.glob("/etc/cron.d/*")):
    sources[path] = _jobs(path)
for path in ("/etc/crontab",):
    sources[path] = _jobs(path)
user_tabs = {}
for path in sorted(glob.glob("/var/spool/cron/*")) + sorted(
    glob.glob("/var/spool/cron/crontabs/*")
):
    user_tabs[os.path.basename(path)] = len(_jobs(path))
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "source_count": len(sources),
    "job_count": sum(len(entries) for entries in sources.values()),
    "sources": sources,
    "user_crontabs": user_tabs,
}
print(json.dumps(report, indent=2))
