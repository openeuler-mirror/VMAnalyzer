#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Monitor PCIe AER errors."""
import json, glob, time as t
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"devices":{}}
for dev in glob.glob("/sys/bus/pci/devices/*/aer_dev_correctable"):
    try:
        addr=dev.split("/")[5]
        with open(dev) as f: d["devices"].setdefault(addr,{})["correctable"]=int(f.read().strip())
    except: pass
for dev in glob.glob("/sys/bus/pci/devices/*/aer_dev_fatal"):
    try:
        addr=dev.split("/")[5]
        with open(dev) as f: d["devices"].setdefault(addr,{})["fatal"]=int(f.read().strip())
    except: pass
print(json.dumps(d,indent=2))
