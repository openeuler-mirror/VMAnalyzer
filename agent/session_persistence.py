#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Persist agent state across restarts."""
import json, os, time, logging, threading
LOG=logging.getLogger(__name__)

class SessionPersistence:
    """Save/restore agent state to survive restarts."""
    def __init__(self,state_file="/var/lib/vmanalyzer/session.json"):
        self.file=state_file; self.state={"vm_list":[],"start_time":time.time(),"collection_count":0}
        self._lock=threading.Lock()
        os.makedirs(os.path.dirname(self.file),exist_ok=True)

    def set(self,key,value):
        with self._lock:
            self.state[key]=value; self._write()

    def get(self,key,default=None):
        return self.state.get(key,default)

    def increment(self,key):
        with self._lock:
            self.state[key]=self.state.get(key,0)+1; self._write()

    def restore(self):
        if os.path.exists(self.file):
            try:
                with open(self.file) as f: self.state.update(json.load(f))
                LOG.info(f"Restored session state from {self.file}")
            except Exception as e: LOG.warning(f"Failed to restore state: {e}")

    def _write(self):
        try:
            with open(self.file,"w") as f: json.dump(self.state,f)
        except Exception as e: LOG.error(f"Failed to write state: {e}")
