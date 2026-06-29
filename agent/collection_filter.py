#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Whitelist/blacklist for VM metric collection."""
import json, os, re, logging
LOG=logging.getLogger(__name__)

class CollectionFilter:
    """Filter VMs for collection based on configurable rules."""
    def __init__(self,config_file="/etc/vmanalyzer/collection_filter.json"):
        self.file=config_file; self.rules=self._load()

    def should_collect(self,vm_name):
        bl=self.rules.get("blacklist",[])
        wl=self.rules.get("whitelist",[])
        if wl and not any(re.match(p,vm_name) for p in wl):
            return False
        if any(re.match(p,vm_name) for p in bl):
            return False
        return True

    def add_blacklist(self,pattern):
        if pattern not in self.rules.setdefault("blacklist",[]):
            self.rules["blacklist"].append(pattern); self._save()

    def add_whitelist(self,pattern):
        if pattern not in self.rules.setdefault("whitelist",[]):
            self.rules["whitelist"].append(pattern); self._save()

    def _load(self):
        if os.path.exists(self.file):
            try:
                with open(self.file) as f: return json.load(f)
            except: pass
        return {"whitelist":[],"blacklist":[]}

    def _save(self):
        os.makedirs(os.path.dirname(self.file),exist_ok=True)
        with open(self.file,"w") as f: json.dump(self.rules,f,indent=2)
