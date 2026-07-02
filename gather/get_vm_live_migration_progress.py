#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Monitor live migration progress."""
import subprocess as sp, json, time as t
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"migrations":{}}
for vm in (sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split()):
    ji=sp.run(f"virsh domjobinfo {vm} 2>&1",shell=True,capture_output=True,text=True).stdout
    if "no job" not in ji.lower():
        info={}
        for ln in ji.split("\\n"):
            if ":" in ln:
                k,v=ln.split(":",1)
                try: info[k.strip()]=int(v.strip())
                except: info[k.strip()]=v.strip()
        d["migrations"][vm]=info
print(json.dumps(d,indent=2))
