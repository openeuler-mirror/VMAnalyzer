#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Monitor TLB flush statistics for performance analysis."""
import subprocess as sp, json, time as t
def diagnose():
    d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"tlb":{}}
    for ln in sp.run("cat /proc/vmstat 2>/dev/null",shell=True,capture_output=True,text=True).stdout.split("\\n"):
        if "tlb" in ln.lower() or "nr_tlb" in ln:
            p=ln.split()
            if len(p)>=2:
                try: d["tlb"][p[0]]=int(p[1])
                except: d["tlb"][p[0]]=p[1]
    d["tlb"]["total_flushes"]=sum(v for k,v in d["tlb"].items() if isinstance(v,int) and "flush" in k.lower())
    print(json.dumps(d,indent=2))
if __name__=="__main__": diagnose()
