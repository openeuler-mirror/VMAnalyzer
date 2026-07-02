#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Manage host affinity and anti-affinity rules."""
import json, os, logging
LOG=logging.getLogger(__name__)

class HostAffinityRules:
    """Define and enforce placement rules for VMs."""
    def __init__(self,rules_file="/etc/vmanalyzer/affinity_rules.json"):
        self.file=rules_file; self.rules={}
        os.makedirs(os.path.dirname(self.file),exist_ok=True)
        if os.path.exists(self.file):
            try:
                with open(self.file) as f: self.rules=json.load(f)
            except: self.rules={}

    def add_affinity(self,vm_a,vm_b,policy="together"):
        self.rules.setdefault("affinity",{})[f"{vm_a}:{vm_b}"]={"type":"affinity","policy":policy}

    def add_anti_affinity(self,vm_a,vm_b):
        self.rules.setdefault("anti_affinity",{})[f"{vm_a}:{vm_b}"]={"type":"anti_affinity","policy":"separate"}

    def check_violation(self,placement):
        violations=[]
        for key,rule in self.rules.get("affinity",{}).items():
            v1,v2=key.split(":")
            if rule["policy"]=="together" and placement.get(v1)!=placement.get(v2):
                violations.append(f"{v1} and {v2} should be together")
        for key,rule in self.rules.get("anti_affinity",{}).items():
            v1,v2=key.split(":")
            if placement.get(v1)==placement.get(v2):
                violations.append(f"{v1} and {v2} should be separate")
        return violations

    def _save(self):
        with open(self.file,"w") as f: json.dump(self.rules,f,indent=2)
