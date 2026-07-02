#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Monitor memory fragmentation via buddyinfo."""
import subprocess as sp, json, time as t
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"zones":{}}
for ln in sp.run("cat /proc/buddyinfo 2>/dev/null",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split("\\n"):
    p=ln.split(); node=" ".join(p[:4])
    orders=[int(x) for x in p[4:] if x.isdigit()]
    d["zones"][node]={"orders":orders,"large_free":sum(orders[-3:]) if len(orders)>=3 else 0}
print(json.dumps(d,indent=2))
