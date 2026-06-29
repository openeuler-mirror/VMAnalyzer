#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Monitor IRQ affinity."""
import subprocess as sp, json, os, time as t
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"irqs":{}}
for vm in (sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split()):
    irqs={}
    for ln in sp.run("cat /proc/interrupts",shell=True,capture_output=True,text=True).stdout.split("\\n"):
        if any(k in ln for k in ["vhost","virtio",vm[:8]]):
            p=ln.split(); irq=p[0].rstrip(":")
            aff="N/A"
            try:
                with open(f"/proc/irq/{irq}/smp_affinity_list") as f: aff=f.read().strip()
            except: pass
            irqs[irq]={"affinity":aff}
    d["irqs"][vm]=irqs
print(json.dumps(d,indent=2))
