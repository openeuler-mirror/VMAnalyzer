#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Centralized timeout configuration for collections."""
import signal, logging
LOG=logging.getLogger(__name__)

class TimeoutManager:
    """Configure per-metric timeouts with defaults."""
    DEFAULTS={"cpu":15,"memory":15,"network":30,"disk":30,"qga":60,"snapshot":120}

    def __init__(self,overrides=None):
        self.timeouts=dict(self.DEFAULTS)
        if overrides: self.timeouts.update(overrides)

    def get(self,metric,default=30):
        return self.timeouts.get(metric,default)

    def set(self,metric,timeout_s):
        self.timeouts[metric]=timeout_s

    def with_timeout(self,func,metric):
        """Call func with timeout; returns None on timeout."""
        import threading
        result=[None]; exc=[None]
        def target():
            try: result[0]=func()
            except Exception as e: exc[0]=e
        t=threading.Thread(target=target,daemon=True); t.start(); t.join(timeout=self.get(metric))
        if t.is_alive():
            LOG.warning("Timeout for %s after %ss" % (metric, self.get(metric)))
            return None
        if exc[0]: raise exc[0]
        return result[0]
