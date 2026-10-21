#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Read block queue depth limits that cap in-flight IO per device."""

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


queues = {}
for path in sorted(glob.glob("/sys/block/*/queue/nr_requests")):
    name = os.path.basename(os.path.dirname(os.path.dirname(path)))
    if name.startswith(("loop", "ram")):
        continue
    queues[name] = {
        "nr_requests": int(_read(path)),
        "max_sectors_kb": int(_read("/sys/block/{}/queue/max_sectors_kb".format(name))),
        "nomerges": int(_read("/sys/block/{}/queue/nomerges".format(name))),
    }
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "queue_count": len(queues),
    "queues": queues,
}
print(json.dumps(report, indent=2))
