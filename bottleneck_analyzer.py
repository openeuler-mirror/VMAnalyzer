#!/usr/bin/env python3
# coding: utf-8
"""
Performance bottleneck root cause analysis
"""
import json
import redis
import libvirt

def analyze_bottlenecks(vm_uuid):
    """Analyze performance bottlenecks for a VM"""
    r = redis.Redis()
    data = r.get(f"vm:{vm_uuid}")
    
    if not data:
        print("❌ No VM metric data found")
        return
    
    metrics = json.loads(data)
    bottlenecks = []
    
    print("=" * 80)
    print(f"🔍 Performance bottleneck root cause analysis - VM: {vm_uuid}")
    print("=" * 80)
    
    # CPU bottleneck
    if metrics.get("cpu_usage", 0) > 90:
        bottlenecks.append("🔴 CPU瓶颈: CPU使用率超过90%")
        if metrics.get("cpu_iowait", 0) > 30:
            bottlenecks.append("   ↳ 根因: IO等待过高，可能是disk性能问题")
        elif metrics.get("context_switches", 0) > 10000:
            bottlenecks.append("   ↳ 根因: 上下文切换频繁，可能是vCPU过载")
    
    # Memory bottleneck
    if metrics.get("memory_usage", 0) > 90:
        bottlenecks.append("🔴 memory瓶颈: memory使用率超过90%")
        if metrics.get("swap_usage", 0) > 50:
            bottlenecks.append("   ↳ 根因: memory不足，正在使用交换分区")
    
    # Disk bottleneck
    if metrics.get("disk_usage", 0) > 90:
        bottlenecks.append("🔴 disk瓶颈: disk使用率超过90%")
    if metrics.get("disk_iops", 0) > 5000:
        bottlenecks.append("🔴 disk瓶颈: IOPS过高")
    
    # Network bottleneck
    if metrics.get("network_usage", 0) > 90:
        bottlenecks.append("🔴 network瓶颈: network带宽使用率超过90%")
    if metrics.get("packet_loss", 0) > 1:
        bottlenecks.append("🔴 network瓶颈: network丢包率过高")
    
    if not bottlenecks:
        print("✅ No obvious performance bottleneck found")
    else:
        for b in bottlenecks:
            print(b)
    
    return bottlenecks

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 bottleneck_analyzer.py <vm_uuid>")
        sys.exit(1)
    analyze_bottlenecks(sys.argv[1])
