#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Check disk I/O throttling configuration."""
import subprocess as sp, json, xml.etree.ElementTree as ET, time as t
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
for vm in (sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split()):
    xml=sp.run(f"virsh dumpxml {vm}",shell=True,capture_output=True,text=True,timeout=30).stdout
    disks={}
    try:
        root=ET.fromstring(xml)
        for disk in root.findall(".//disk"):
            tgt=disk.find("target"); dev=tgt.get("dev") if tgt is not None else "?"
            iotune=disk.find("iotune")
            disks[dev]={c.tag:c.text for c in iotune} if iotune is not None else {"throttled":False}
    except: pass
    d["vms"][vm]=disks
print(json.dumps(d,indent=2))
