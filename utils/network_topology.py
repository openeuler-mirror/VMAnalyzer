#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Map VM network topology."""
import subprocess as sp, json, logging
LOG=logging.getLogger(__name__)

class NetworkTopology:
    """Discover network connections between VMs and bridges."""
    @staticmethod
    def get_bridges():
        bridges=[]
        for ln in sp.run("brctl show 2>/dev/null||ip link show type bridge",shell=True,capture_output=True,text=True).stdout.split("\\n"):
            p=ln.split()
            if p and ":" not in p[0] and p[0]!="bridge": bridges.append(p[0])
        return bridges

    @staticmethod
    def get_vm_networks():
        nets={}
        for vm in sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True).stdout.strip().split():
            ifaces=[]
            for ln in sp.run(f"virsh domiflist {vm}",shell=True,capture_output=True,text=True).stdout.split("\\n")[2:]:
                p=ln.split()
                if p and p[0]!="-": ifaces.append({"iface":p[0],"type":p[1] if len(p)>1 else "","source":p[2] if len(p)>2 else ""})
            nets[vm]=ifaces
        return {"bridges":NetworkTopology.get_bridges(),"vms":nets}
