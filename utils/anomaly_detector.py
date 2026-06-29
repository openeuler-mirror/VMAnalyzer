#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Statistical anomaly detection for VM metrics."""
import statistics, logging
LOG=logging.getLogger(__name__)

class AnomalyDetector:
    """Detect anomalies using z-score and moving average methods."""
    def __init__(self, window_size=30, threshold=3.0):
        self.window_size=window_size
        self.threshold=threshold
        self.data=[]

    def add(self,value):
        self.data.append(value)
        if len(self.data)>self.window_size*2: self.data=self.data[-self.window_size*2:]

    def is_anomaly(self,value):
        if len(self.data)<self.window_size: return False
        recent=self.data[-self.window_size:]
        mu=statistics.mean(recent)
        sigma=statistics.stdev(recent) if len(recent)>1 else 1
        z=abs(value-mu)/sigma if sigma>0 else 0
        return z>self.threshold

    def detect(self,values):
        results=[]
        for v in values:
            self.add(v)
            results.append({"value":v,"anomaly":self.is_anomaly(v),"z_score":abs(v-statistics.mean(self.data[-self.window_size:]))/max(statistics.stdev(self.data[-self.window_size:]),1e-6)})
        return results
