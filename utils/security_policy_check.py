#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Check VM configurations against security policies."""
import subprocess as sp, json, logging
LOG=logging.getLogger(__name__)

class SecurityPolicyCheck:
    """Validate VMs against security best practices."""
    CHECKS = {
        "no_default_network": "Check VMs are not on default network",
        "no_spice_insecure": "Check SPICE is not in insecure mode",
        "selinux_enforcing": "Verify SELinux is enforcing on host",
        "apparmor_enabled": "Verify AppArmor is active if applicable",
    }

    @staticmethod
    def check_vm(vm_name):
        xml=sp.run(f"virsh dumpxml {vm_name}",shell=True,capture_output=True,text=True).stdout
        results={}
        results["default_network"]="default" not in xml
        results["no_clear_text_console"]="listen=0.0.0.0" not in xml
        results["seclabel_present"]="<seclabel" in xml
        return results

    @staticmethod
    def check_host():
        r={}
        sel=sp.run("getenforce 2>/dev/null",shell=True,capture_output=True,text=True).stdout.strip()
        r["selinux"]=sel if sel else "disabled"
        return r
