#!/usr/bin/env python3
"""
Generate scheduled performance report
"""
import json
import redis
from datetime import datetime, timedelta

def generate_daily_report():
    """Generate daily performance report"""
    r = redis.Redis()
    keys = r.keys("vm:*")
    
    report = {
        "report_type": "daily",
        "generated_at": datetime.now().isoformat(),
        "period": f"{(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}",
        "vm_count": len(keys),
        "summary": []
    }
    
    for key in keys:
        data = json.loads(r.get(key))
        report["summary"].append({
            "vm_uuid": key.decode(),
            "avg_cpu_usage": data.get("cpu_usage", 0),
            "avg_memory_usage": data.get("memory_usage", 0),
            "max_disk_usage": data.get("disk_usage", 0)
        })
    
    output_file = f"daily_report_{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 日报已生成: {output_file}")
    return report

if __name__ == "__main__":
    generate_daily_report()
