#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Summarise loaded kernel modules with the heaviest consumers."""

import json
import time as t


def _modules():
    rows = []
    try:
        with open("/proc/modules", "r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                fields = line.split()
                if len(fields) < 3:
                    continue
                try:
                    size = int(fields[1])
                except ValueError:
                    continue
                rows.append(
                    {
                        "name": fields[0],
                        "size": size,
                        "instances": int(fields[2]),
                    }
                )
    except OSError:
        return rows
    return rows


modules = _modules()
modules.sort(key=lambda item: item["size"], reverse=True)
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "module_count": len(modules),
    "total_size": sum(item["size"] for item in modules),
    "top_modules": modules[:10],
}
print(json.dumps(report, indent=2))
