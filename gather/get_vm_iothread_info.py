#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Collect IOThread configuration."""
import subprocess as sp, json, time as t
SP=lambda c:sp.run(c,shell=True,capture_output=True,text=True,timeout=30).stdout.strip()
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
for vm in (SP("virsh list --name|grep -v ^$|grep -v ^-$").split()):
    d["vms"][vm]={"iothreads":SP(f"virsh iothreadinfo {vm}"),"pin":SP(f"virsh iothreadpin {vm}")}
print(json.dumps(d,indent=2))
