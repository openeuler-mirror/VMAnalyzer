#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Count audit rules and their sources for compliance review."""

import glob
import json
import time as t


def _lines(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.readlines()
    except OSError:
        return []


def _rules(path):
    rules = []
    for line in _lines(path):
        text = line.strip()
        if text and not text.startswith("#"):
            rules.append(text)
    return rules


sources = {}
total = 0
for path in ["/etc/audit/audit.rules"] + sorted(glob.glob("/etc/audit/rules.d/*.rules")):
    rules = _rules(path)
    sources[path] = {"count": len(rules), "rules": rules[:10]}
    total += len(rules)
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "rule_count": total,
    "source_count": len(sources),
    "sources": sources,
}
print(json.dumps(report, indent=2))
