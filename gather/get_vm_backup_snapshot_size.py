#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Collect snapshot and storage info."""
import subprocess as sp, json, shlex, time as t
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
listing=sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30)
for vm in [ln.strip() for ln in listing.stdout.split("\n") if ln.strip()]:
    snaps=sp.run(f"virsh snapshot-list {shlex.quote(vm)} 2>/dev/null",shell=True,capture_output=True,text=True).stdout
    count=max(len([l for l in snaps.split("\n")[2:] if l.strip()]),0)
    d["vms"][vm]={"snapshot_count":count}
print(json.dumps(d,indent=2))
