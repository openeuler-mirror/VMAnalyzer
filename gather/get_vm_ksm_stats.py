#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Collect Kernel Same-page Merging statistics."""
import json, os, time as t
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"ksm":{}}
ks="/sys/kernel/mm/ksm"
for f in ["run","pages_shared","pages_sharing","pages_unshared","full_scans"]:
    try:
        with open(os.path.join(ks,f)) as fh: d["ksm"][f]=int(fh.read().strip())
    except: d["ksm"][f]=None
d["ksm"]["active"]=d["ksm"].get("run",0)>0
if d["ksm"].get("pages_sharing") and d["ksm"].get("pages_shared"):
    d["ksm"]["saved_bytes"]=(d["ksm"]["pages_sharing"]-d["ksm"]["pages_shared"])*4096
print(json.dumps(d,indent=2))
