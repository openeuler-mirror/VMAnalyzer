#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Analyze VM disk I/O performance."""
import subprocess as sp, json, shlex, time as t
def diagnose():
    d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
    listing=sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30)
    for vm in [ln.strip() for ln in listing.stdout.split("\n") if ln.strip()]:
        devs={}
        blk=sp.run(f"virsh domblklist {shlex.quote(vm)} --details",shell=True,capture_output=True,text=True).stdout
        for ln in blk.split("\n")[2:]:
            p=ln.split()
            if len(p)<3 or not p[1]: continue
            dev=p[1]
            bs=sp.run(f"virsh domblkstat {shlex.quote(vm)} {shlex.quote(dev)}",shell=True,capture_output=True,text=True).stdout
            s={}
            for l in bs.split("\n"):
                kv=l.split()
                if len(kv)>=2:
                    try: s[kv[0]]=int(kv[1])
                    except ValueError: pass
            errors=s.get("errs",0)
            devs[dev]={"errors":errors,"read_bytes":s.get("rd_bytes",0),"write_bytes":s.get("wr_bytes",0)}
        d["vms"][vm]=devs
    print(json.dumps(d,indent=2))
if __name__=="__main__": diagnose()
