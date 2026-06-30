#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Enable hugepages for VM performance."""
import subprocess as sp, json, os, sys, time as t
def main():
    size=sys.argv[1] if len(sys.argv)>1 else "2048"
    count=sys.argv[2] if len(sys.argv)>2 else "1024"
    result={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"actions":[]}
    # Check current
    for hp in os.listdir("/sys/kernel/mm/hugepages"):
        try:
            with open(f"/sys/kernel/mm/hugepages/{hp}/nr_hugepages") as f:
                result["before"]={"size":hp,"nr":int(f.read().strip())}
        except: pass
    # Set
    try:
        with open(f"/sys/kernel/mm/hugepages/hugepages-{size}kB/nr_hugepages","w") as f:
            f.write(count)
        result["actions"].append(f"set_{size}kB_to_{count}")
        result["success"]=True
    except PermissionError:
        result["actions"].append("permission_denied_need_root")
        result["success"]=False
    except FileNotFoundError:
        result["actions"].append("hugepage_size_unavailable")
        result["success"]=False
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()
