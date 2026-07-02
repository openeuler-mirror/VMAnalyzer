#!/usr/bin/env python3
# coding: utf-8
"""
Export VM metrics to JSON format
"""
import json
import redis
from datetime import datetime

r = redis.Redis()
keys = r.keys("vm:*")
export_data = []

for key in keys:
    raw = r.get(key)
    if raw is None:
        continue
    data = json.loads(raw)
    export_data.append({
        "vm_uuid": key.decode(),
        "metrics": data,
        "export_time": datetime.now().isoformat()
    })

output_file = f"vm_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(output_file, "w") as f:
    json.dump(export_data, f, indent=2, ensure_ascii=False)

print(f"✅ 指标已导出到: {output_file}")
