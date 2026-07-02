#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Monitor agent own resource usage."""
import os, psutil, time, threading, logging
LOG=logging.getLogger(__name__)

class SelfMonitor:
    """Track agent CPU, memory, and FD usage."""
    def __init__(self):
        self.process=psutil.Process(os.getpid())
        self.metrics={}; self._stop=False
        self._thread=None

    def _collect(self,interval=30):
        while not self._stop:
            try:
                self.metrics={"cpu_pct":self.process.cpu_percent(),"mem_mb":self.process.memory_info().rss/1024/1024,"fds":self.process.num_fds(),"threads":self.process.num_threads(),"uptime_s":time.time()-self.process.create_time(),"timestamp":time.time()}
                LOG.debug(f"Self-monitor: {self.metrics}")
            except Exception as e: LOG.warning(f"Self-monitor error: {e}")
            time.sleep(interval)

    def start(self,interval=30):
        self._thread=threading.Thread(target=self._collect,args=(interval,),daemon=True)
        self._thread.start()

    def stop(self):
        self._stop=True; self._thread and self._thread.join(timeout=5)

    def get_metrics(self):
        return dict(self.metrics)
