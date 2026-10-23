#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Check disk I/O alignment for optimal performance."""
import subprocess as sp, json, shlex, time as t
def diagnose():
    d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
    listing=sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30)
    for vm in [ln.strip() for ln in listing.stdout.split("\n") if ln.strip()]:
        blk=sp.run(f"virsh domblklist {shlex.quote(vm)} --details",shell=True,capture_output=True,text=True).stdout
        devs=[]
        for ln in blk.split("\n")[2:]:
            p=ln.split()
            if len(p)<3 or not p[1]: continue
            dev=p[1]
            info=sp.run(f"virsh domblkinfo {shlex.quote(vm)} {shlex.quote(dev)}",shell=True,capture_output=True,text=True).stdout
            align={"dev":dev,"type":p[0]}
            for l in info.split("\n"):
                if "Allocation" in l:
                    try:
                        val=int(l.split(":")[-1].strip())
                        align["allocation"]=val
                        align["aligned"]=(val%4096==0) if val>0 else True
                    except ValueError: pass
            devs.append(align)
        d["vms"][vm]=devs
    print(json.dumps(d,indent=2))
if __name__=="__main__": diagnose()
