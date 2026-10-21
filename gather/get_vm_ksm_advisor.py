#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Report KSM sharing benefit so operators can judge merge payoff."""

import json
import time as t


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read().strip()
    except OSError:
        return ""


def _stat(name):
    value = _read("/sys/kernel/mm/ksm/" + name)
    return int(value) if value.isdigit() else 0


shared = _stat("pages_shared")
sharing = _stat("pages_sharing")
unshared = _stat("pages_unshared")
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "running": _read("/sys/kernel/mm/ksm/run") or "0",
    "merge_across_nodes": _read("/sys/kernel/mm/ksm/merge_across_nodes") or "unknown",
    "pages_shared": shared,
    "pages_sharing": sharing,
    "pages_unshared": unshared,
    "saved_mb": round(sharing * 4.0 / 1024.0, 2),
    "benefit_ratio": round(sharing / float(sharing + unshared), 4)
    if sharing + unshared
    else 0.0,
}
print(json.dumps(report, indent=2))
