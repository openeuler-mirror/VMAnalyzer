#!/usr/bin/env python3
"""
Export VM metrics to CSV file
"""
import csv
import redis
import json
from datetime import datetime

r = redis.Redis()
keys = r.keys("vm:*")

with open(f"vm_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["VM UUID", "CPU Usage (%)", "Memory Usage (%)", "Timestamp"])
    
    for key in keys:
        data = json.loads(r.get(key))
        writer.writerow([
            key.decode(),
            data.get("cpu_usage", ""),
            data.get("memory_usage", ""),
            data.get("timestamp", "")
        ])
