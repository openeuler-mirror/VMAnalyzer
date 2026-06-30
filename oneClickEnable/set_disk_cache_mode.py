#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Configure disk cache mode for VM performance."""
import subprocess as sp, json, xml.etree.ElementTree as ET, sys, time as t
CACHE_MODES=["none","writethrough","writeback","directsync","unsafe"]
def main():
    vm=sys.argv[1] if len(sys.argv)>1 else None
    mode=sys.argv[2] if len(sys.argv)>2 else "none"
    result={"vm":vm,"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime())}
    if not vm:
        result["error"]="Usage: set_disk_cache_mode.py <vm_name> [cache_mode]"
        result["modes"]=CACHE_MODES
        print(json.dumps(result,indent=2)); return 1
    xml=sp.run(f"virsh dumpxml {vm}",shell=True,capture_output=True,text=True).stdout
    disks=[]
    try:
        root=ET.fromstring(xml)
        for disk in root.findall(".//disk"):
            tgt=disk.find("target"); dev=tgt.get("dev") if tgt is not None else "?"
            driver=disk.find("driver"); cache=driver.get("cache","default") if driver is not None else "default"
            disks.append({"dev":dev,"current_cache":cache})
    except: pass
    result["disks"]=disks
    result["recommended"]="Use none or writeback for performance; none for data safety"
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()
