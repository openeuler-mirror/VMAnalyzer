#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Collect vhost-net queue info."""
import subprocess as sp, json, glob, time as t
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
for vm in (sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split()):
    ps=sp.run(f"ps aux|grep qemu.*{vm}|grep -v grep",shell=True,capture_output=True,text=True).stdout
    for ln in ps.split("\\n"):
        p=ln.split()
        if len(p)>=2:
            try:
                pid=int(p[1])
                d["vms"][vm]={"pid":pid,"threads":len(glob.glob(f"/proc/{pid}/task/*")),"fds":len(glob.glob(f"/proc/{pid}/fd/*"))}
                break
            except: pass
print(json.dumps(d,indent=2))
