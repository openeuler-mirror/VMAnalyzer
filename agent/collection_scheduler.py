#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Cron-like scheduling for metric collections."""
import time
import logging, sched, threading
LOG=logging.getLogger(__name__)

class CollectionScheduler:
    """Schedule different metrics at different intervals."""
    def __init__(self):
        self._scheduler=sched.scheduler(time.time,time.sleep)
        self._jobs={}; self._running=False

    def add_job(self,name,func,interval_s):
        self._jobs[name]={"func":func,"interval":interval_s,"last_run":0}

    def _run_jobs(self):
        now=time.time()
        for name,job in self._jobs.items():
            if now-job["last_run"]>=job["interval"]:
                try:
                    job["func"](); job["last_run"]=now
                    LOG.debug(f"Scheduled job {name} ran")
                except Exception as e: LOG.error(f"Job {name} failed: {e}")

    def start(self,tick_s=1):
        self._running=True
        def loop():
            while self._running:
                self._run_jobs(); time.sleep(tick_s)
        self._thread=threading.Thread(target=loop,daemon=True); self._thread.start()

    def stop(self):
        self._running=False
