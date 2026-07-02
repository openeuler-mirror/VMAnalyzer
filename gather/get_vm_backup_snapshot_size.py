#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Collect snapshot and storage info."""
import subprocess as sp, json, time as t
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
for vm in (sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split()):
    snaps=sp.run(f"virsh snapshot-list {vm} 2>/dev/null",shell=True,capture_output=True,text=True).stdout
    count=len(snaps.split("\\n"))-2 if snaps else 0
    d["vms"][vm]={"snapshot_count":count}
print(json.dumps(d,indent=2))
