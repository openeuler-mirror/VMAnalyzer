#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Rate limiter for QGA commands to prevent flooding."""
import time, threading, logging
LOG=logging.getLogger(__name__)

class QGARateLimiter:
    """Limit QGA command rate per VM or globally."""
    def __init__(self,max_per_second=5):
        self.rate=max_per_second; self.window = 1.0 / max_per_second if max_per_second > 0 else 0
        self._last={}; self._lock=threading.Lock()

    def acquire(self,vm_name):
        if self.window<=0: return True
        with self._lock:
            now=time.time(); last=self._last.get(vm_name,0)
            wait=self.window-(now-last)
            if wait>0:
                LOG.debug(f"Rate limiting {vm_name}: waiting {wait:.3f}s")
                time.sleep(wait)
            self._last[vm_name]=time.time()
        return True

    def reset(self,vm_name=None):
        with self._lock:
            if vm_name:
                self._last.pop(vm_name,None)
            else:
                self._last.clear()

    def check(self,vm_name):
        with self._lock:
            now=time.time()
            last=self._last.get(vm_name)
            if last is None:
                return True
            return now-last>=self.window
