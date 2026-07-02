#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Analyze correlations between VM metrics."""
import statistics, math, logging
LOG=logging.getLogger(__name__)

class CorrelationAnalyzer:
    """Compute Pearson correlation between two metric series."""
    @staticmethod
    def pearson(xs,ys):
        n=len(xs)
        if n<3 or n!=len(ys): return None
        mx=statistics.mean(xs); my=statistics.mean(ys)
        num=sum((x-mx)*(y-my) for x,y in zip(xs,ys))
        dx=math.sqrt(sum((x-mx)**2 for x in xs))
        dy=math.sqrt(sum((y-my)**2 for y in ys))
        if dx==0 or dy==0: return 0
        r=num/(dx*dy)
        if abs(r)>0.7: strength="strong"
        elif abs(r)>0.4: strength="moderate"
        else: strength="weak"
        return {"coefficient":round(r,4),"strength":strength,"samples":n}

    @staticmethod
    def find_correlated(metrics,threshold=0.7):
        keys=list(metrics.keys()); pairs=[]
        for i in range(len(keys)):
            for j in range(i+1,len(keys)):
                r=CorrelationAnalyzer.pearson(metrics[keys[i]],metrics[keys[j]])
                if r and abs(r["coefficient"])>=threshold:
                    pairs.append({"metric1":keys[i],"metric2":keys[j],"correlation":r})
        return sorted(pairs,key=lambda x:abs(x["correlation"]["coefficient"]),reverse=True)
