#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Pluggable hooks for VM lifecycle events."""
import logging
LOG=logging.getLogger(__name__)

class LifecycleHooks:
    """Register callbacks for VM start/stop/pause/resume/migrate events."""
    HOOKS=["on_vm_start","on_vm_stop","on_vm_pause","on_vm_resume","on_vm_migrate","on_vm_crash"]

    def __init__(self):
        self._hooks={h:[] for h in self.HOOKS}

    def register(self,hook_name,callback):
        if hook_name in self._hooks:
            self._hooks[hook_name].append(callback)
            LOG.info(f"Registered hook: {hook_name}")

    def trigger(self,hook_name,**kwargs):
        results=[]
        if hook_name not in self._hooks: return results
        for cb in self._hooks[hook_name]:
            try: results.append(cb(**kwargs))
            except Exception as e: LOG.error(f"Hook {hook_name} failed: {e}")
        return results

    def get_hook_count(self):
        return {k:len(v) for k,v in self._hooks.items()}
