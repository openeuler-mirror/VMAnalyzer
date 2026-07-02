#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Analyze performance trends over time."""
import statistics, time, logging
LOG=logging.getLogger(__name__)

class TrendAnalyzer:
    """Calculate linear regression trend on metric time series."""
    def __init__(self,window_minutes=30):
        self.window=window_minutes
        self.series=[]

    def add_point(self,value,timestamp=None):
        ts=timestamp or time.time()
        self.series.append((ts,value))
        cutoff=time.time()-self.window*60
        self.series=[(t,v) for t,v in self.series if t>=cutoff]

    def get_trend(self):
        n=len(self.series)
        if n<3: return {"direction":"stable","slope":0}
        xs=[i for i in range(n)]; ys=[v for _,v in self.series]
        mx=statistics.mean(xs); my=statistics.mean(ys)
        num=sum((x-mx)*(y-my) for x,y in zip(xs,ys))
        den=sum((x-mx)**2 for x in xs)
        slope=num/den if den else 0
        if slope>0.01: d="up"
        elif slope<-0.01: d="down"
        else: d="stable"
        return {"direction":d,"slope":round(slope,4),"points":n}
