#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Detect nested virtualization capability."""
import subprocess as sp
import json
import time as t
import shlex
import logging
LOG = logging.getLogger(__name__)
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"nested":{}}
r=sp.run("cat /sys/module/kvm_intel/parameters/nested 2>/dev/null||cat /sys/module/kvm_amd/parameters/nested 2>/dev/null",shell=True,capture_output=True,text=True).stdout.strip()
d["nested"]["host_nested"]=r if r else "unknown"
cpu=sp.run("grep -Ec \"(vmx|svm)\" /proc/cpuinfo",shell=True,capture_output=True,text=True).stdout.strip()
d["nested"]["cpu_virt_cores"]=int(cpu) if cpu.isdigit() else 0
LOG.debug(json.dumps(d,indent=2))
