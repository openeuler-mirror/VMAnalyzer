#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Configure CPU model passthrough for VMs."""
import subprocess as sp, json, sys, xml.etree.ElementTree as ET, time as t
def main():
    vm=sys.argv[1] if len(sys.argv)>1 else None
    if not vm:
        print(json.dumps({"error":"Usage: set_cpu_passthrough.py <vm_name>"})); return 1
    result={"vm":vm,"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime())}
    xml=sp.run("virsh dumpxml %s" % vm,shell=True,capture_output=True,text=True).stdout
    try:
        root=ET.fromstring(xml); cpu=root.find("cpu")
        if cpu is not None and cpu.get("mode")=="host-passthrough":
            result["status"]="already_host-passthrough"
        else:
            result["status"]="needs_manual_edit"
            result["hint"]="virsh edit <vm> and set <cpu mode=\"host-passthrough\" check=\"none\"/>"
    except Exception as e:
        result["error"]=str(e)
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()
