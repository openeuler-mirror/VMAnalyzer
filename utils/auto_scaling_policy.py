#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Auto-scaling policy management for VMs."""
import time, logging
LOG=logging.getLogger(__name__)

class AutoScalingPolicy:
    """Define and evaluate auto-scaling rules."""
    def __init__(self):
        self.policies=[]

    def add_rule(self,vm_match,metric,threshold,action,cooldown_s=300):
        self.policies.append({"vm":vm_match,"metric":metric,"threshold":threshold,"action":action,"cooldown":cooldown_s,"last_action":0})

    def evaluate(self,vms_metrics):
        actions=[]
        now=time.time()
        for p in self.policies:
            for vm_name,metrics in vms_metrics.items():
                if p["vm"] not in vm_name: continue
                value=metrics.get(p["metric"])
                if value is None: continue
                if (p["action"].startswith("scale_up") and value>p["threshold"]) or (p["action"].startswith("scale_down") and value<p["threshold"]):
                    if now-p["last_action"]>=p["cooldown"]:
                        actions.append({"vm":vm_name,"action":p["action"],"metric":p["metric"],"value":value,"threshold":p["threshold"]})
                        p["last_action"]=now
        return actions
