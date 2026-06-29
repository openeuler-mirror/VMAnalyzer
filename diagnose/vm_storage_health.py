#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Check VM storage pool health."""
import subprocess as sp, json, time as t
def diagnose():
    d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"pools":{}}
    pools=sp.run("virsh pool-list --all 2>/dev/null",shell=True,capture_output=True,text=True).stdout
    for ln in pools.split("\\n")[2:]:
        p=ln.split()
        if len(p)>=3:
            name=p[0]; state=p[1]
            info=sp.run(f"virsh pool-info {name} 2>/dev/null",shell=True,capture_output=True,text=True).stdout
            pi={}
            for l in info.split("\\n"):
                if ":" in l:
                    k,v=l.split(":",1); pi[k.strip()]=v.strip()
            d["pools"][name]={"state":state,"info":pi,"healthy":state.lower()=="running" or state.lower()=="active"}
    print(json.dumps(d,indent=2))
if __name__=="__main__": diagnose()
