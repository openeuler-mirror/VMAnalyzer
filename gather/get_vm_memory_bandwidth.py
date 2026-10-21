#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Sample page in/out throughput to estimate memory bandwidth."""

import json
import time as t

WINDOW = 2.0


def _vmstat():
    values = {}
    try:
        with open("/proc/vmstat", "r", encoding="utf-8") as handle:
            for line in handle:
                fields = line.split()
                if len(fields) == 2 and fields[1].isdigit():
                    values[fields[0]] = int(fields[1])
    except OSError:
        return values
    return values


first = _vmstat()
t.sleep(WINDOW)
second = _vmstat()
pages_in = second.get("pgpgin", 0) - first.get("pgpgin", 0)
pages_out = second.get("pgpgout", 0) - first.get("pgpgout", 0)
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "window_seconds": WINDOW,
    "read_kb_per_second": round(pages_in / WINDOW, 2),
    "write_kb_per_second": round(pages_out / WINDOW, 2),
    "total_mb_per_second": round((pages_in + pages_out) / WINDOW / 1024.0, 3),
}
print(json.dumps(report, indent=2))
