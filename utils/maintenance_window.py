#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Schedule and manage maintenance windows."""
import json, os, time, logging
LOG=logging.getLogger(__name__)

class MaintenanceWindow:
    """Define and check if current time is in a maintenance window."""
    def __init__(self,config_path="/etc/vmanalyzer/maintenance.json"):
        self.path=config_path; self.windows=[]
        os.makedirs(os.path.dirname(self.path),exist_ok=True)
        if os.path.exists(self.path):
            try:
                with open(self.path) as f: self.windows=json.load(f)
            except: pass

    def add_window(self,start_ts,end_ts,vm_list,reason=""):
        w={"start":start_ts,"end":end_ts,"vms":vm_list,"reason":reason}
        self.windows.append(w); self._save()

    def is_active(self,vm_name,now=None):
        now=now or time.time()
        for w in self.windows:
            if w["start"]<=now<=w["end"] and (vm_name in w.get("vms",[]) or not w.get("vms")):
                return True
        return False

    def upcoming(self,vm_name,now=None):
        now=now or time.time()
        return [w for w in self.windows if w["start"]>now and vm_name in w.get("vms",[])]

    def _save(self):
        with open(self.path,"w") as f: json.dump(self.windows,f,indent=2)
