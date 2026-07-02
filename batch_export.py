#!/usr/bin/env python3
# coding: utf-8
"""
Batch export all VM metrics in multiple formats
"""
import json
import csv
import redis
from datetime import datetime

def export_all(formats=['json', 'csv']):
    """Export all VM metrics in specified formats"""
    r = redis.Redis()
    keys = r.keys("vm:*")
    all_data = []
    
    for key in keys:
        data = json.loads(r.get(key))
        data['vm_uuid'] = key.decode()
        all_data.append(data)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if 'json' in formats:
        with open(f"batch_export_{timestamp}.json", "w") as f:
            json.dump(all_data, f, indent=2)
        print(f"✅ JSON导出完成: batch_export_{timestamp}.json")
    
    if 'csv' in formats:
        if all_data and any(data for data in all_data):
            with open(f"batch_export_{timestamp}.csv", "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=all_data[0].keys())
                writer.writeheader()
                writer.writerows(all_data)
            print(f"✅ CSV导出完成: batch_export_{timestamp}.csv")
    
    return all_data

if __name__ == "__main__":
    export_all()
