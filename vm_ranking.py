#!/usr/bin/env python3
# coding: utf-8
"""
VM resource usage ranking
"""
import json
import redis

def get_vm_ranking(sort_by="cpu_usage", limit=10):
    """Get VM ranking by resource usage"""
    r = redis.Redis()
    keys = r.keys("vm:*")
    vms = []
    
    for key in keys:
        data = json.loads(r.get(key))
        data['vm_uuid'] = key.decode()
        vms.append(data)
    
    # Sort entries.
    vms.sort(key=lambda x: x.get(sort_by, 0), reverse=True)
    
    print("=" * 80)
    print(f"🏆 VM资源使用排名 (按 {sort_by} 降序)")
    print("=" * 80)
    print(f"{'Operation message':<4} {'VM UUID':<40} {'Operation message':<10} {'Operation message'}")
    print("-" * 80)
    
    units = {
        "cpu_usage": "%",
        "memory_usage": "%", 
        "disk_usage": "%",
        "network_tx": "MB/s",
        "network_rx": "MB/s"
    }
    unit = units.get(sort_by, "")
    
    for i, vm in enumerate(vms[:limit], 1):
        value = vm.get(sort_by, 0)
        print(f"{i:<4} {vm['vm_uuid']:<40} {value:<10.1f} {unit}")
    
    return vms

if __name__ == "__main__":
    import sys
    sort_by = sys.argv[1] if len(sys.argv) > 1 else "cpu_usage"
    get_vm_ranking(sort_by)
