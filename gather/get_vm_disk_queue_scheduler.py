#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Check disk I/O scheduler."""
import json, glob, time as t
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"devices":{}}
for dev in glob.glob("/sys/block/*/queue/scheduler"):
    try:
        with open(dev) as f: d["devices"][dev.split("/")[3]]=f.read().strip()
    except: pass
print(json.dumps(d,indent=2))
