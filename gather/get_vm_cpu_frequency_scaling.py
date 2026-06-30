#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Monitor CPU frequency scaling."""
import json, os, glob, time as t
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"cpus":{}}
for cd in glob.glob("/sys/devices/system/cpu/cpu[0-9]*/cpufreq"):
    cpu=cd.split("/cpu")[1].split("/")[0]; info={}
    for f in ["scaling_cur_freq","scaling_governor","scaling_max_freq"]:
        try:
            with open(os.path.join(cd,f)) as fh: info[f]=fh.read().strip()
        except: info[f]=None
    d["cpus"][cpu]=info
print(json.dumps(d,indent=2))
