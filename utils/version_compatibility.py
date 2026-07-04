#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Check version compatibility between components."""
import subprocess as sp, re, logging
LOG=logging.getLogger(__name__)

class VersionCompatibility:
    """Verify libvirt, QEMU, and kernel versions are compatible."""
    @staticmethod
    def get_libvirt_version():
        r=sp.run("libvirtd --version 2>/dev/null||virsh version --short 2>/dev/null",shell=True,capture_output=True,text=True).stdout.strip()
        nums=re.findall(r"\d+", r); return [int(x) for x in nums[:3]] if nums else []

    @staticmethod
    def get_qemu_version():
        r=sp.run("qemu-system-x86_64 --version 2>/dev/null",shell=True,capture_output=True,text=True).stdout.strip()
        nums=re.findall(r"\d+", r); return [int(x) for x in nums[:3]] if nums else []

    @staticmethod
    def check_compatibility():
        lv=VersionCompatibility.get_libvirt_version(); qv=VersionCompatibility.get_qemu_version()
        issues=[]
        if lv and lv[0]<5: issues.append("libvirt too old (<5.x)")
        if qv and qv[0]<3: issues.append("QEMU too old (<3.x)")
        return {"libvirt":lv,"qemu":qv,"compatible":len(issues)==0,"issues":issues}
