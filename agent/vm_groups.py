#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""VM grouping and tagging for organized monitoring."""
import json, os, logging
LOG=logging.getLogger(__name__)
GROUPS_FILE="/var/lib/vmanalyzer/vm_groups.json"

class VMGroupManager:
    """Categorize VMs into groups for batch operations."""
    def __init__(self):
        self.groups=self._load()

    def add_group(self,name,tags=None):
        self.groups[name]={"vms":[],"tags":tags or []}; self._save()

    def add_vm(self,group,vm_name):
        if group in self.groups:
            if vm_name not in self.groups[group]["vms"]:
                self.groups[group]["vms"].append(vm_name); self._save()

    def remove_vm(self,group,vm_name):
        if group in self.groups and vm_name in self.groups[group]["vms"]:
            self.groups[group]["vms"].remove(vm_name); self._save()

    def get_vms(self,group):
        return self.groups.get(group,{}).get("vms",[])

    def list_groups(self):
        return {k:{vms:len(v.get(vms,[])),tags:v.get(tags,[])} for k,v in self.groups.items()}

    def _load(self):
        if os.path.exists(GROUPS_FILE):
            try:
                with open(GROUPS_FILE) as f: return json.load(f)
            except: return {}
        return {}

    def _save(self):
        os.makedirs(os.path.dirname(GROUPS_FILE),exist_ok=True)
        with open(GROUPS_FILE,"w") as f: json.dump(self.groups,f,indent=2)
