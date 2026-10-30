#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Collect NUMA topology for VMs."""
import subprocess as sp
import json
import time as t
import shlex
SP=lambda c:sp.run(c,shell=True,capture_output=True,text=True,timeout=30).stdout.strip()
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
for vm in (SP("virsh list --name|grep -v ^$|grep -v ^-$").split()):
    d["vms"][vm]={"vcpu_pin":SP(f"virsh vcpupin {shlex.quote(str(vm))}"),"emulator_pin":SP(f"virsh emulatorpin {shlex.quote(str(vm))}"),"numa":SP(f"virsh numatune {shlex.quote(str(vm))}")}
print(json.dumps(d,indent=2))
