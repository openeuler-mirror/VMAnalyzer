#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""List configured huge page sizes with total and free counts."""

import glob
import json
import os
import time as t


def _read(path, default="0"):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read().strip()
    except OSError:
        return default


pages = {}
for path in sorted(glob.glob("/sys/kernel/mm/hugepages/hugepages-*")):
    size_kb = os.path.basename(path).split("-")[-1].replace("kb", "")
    pages[size_kb] = {
        "nr_hugepages": int(_read(path + "/nr_hugepages")),
        "free_hugepages": int(_read(path + "/free_hugepages")),
        "resv_hugepages": int(_read(path + "/resv_hugepages")),
    }
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "sizes": pages,
    "thp_enabled": _read("/sys/kernel/mm/transparent_hugepage/enabled", "unknown"),
}
print(json.dumps(report, indent=2))
