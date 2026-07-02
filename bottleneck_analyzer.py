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
        print("❌ 未找到VM指标数据")
        return
    
    metrics = json.loads(data)
    bottlenecks = []
    
    print("=" * 80)
    print(f"🔍 性能瓶颈根因分析 - VM: {vm_uuid}")
    print("=" * 80)
    
    # CPU bottleneck
    if metrics.get("cpu_usage", 0) > 90:
        bottlenecks.append("🔴 CPU瓶颈: CPU使用率超过90%")
        if metrics.get("cpu_iowait", 0) > 30:
            bottlenecks.append("   ↳ 根因: IO等待过高，可能是磁盘性能问题")
        elif metrics.get("context_switches", 0) > 10000:
            bottlenecks.append("   ↳ 根因: 上下文切换频繁，可能是vCPU过载")
    
    # Memory bottleneck
    if metrics.get("memory_usage", 0) > 90:
        bottlenecks.append("🔴 内存瓶颈: 内存使用率超过90%")
        if metrics.get("swap_usage", 0) > 50:
            bottlenecks.append("   ↳ 根因: 内存不足，正在使用交换分区")
    
    # Disk bottleneck
    if metrics.get("disk_usage", 0) > 90:
        bottlenecks.append("🔴 磁盘瓶颈: 磁盘使用率超过90%")
    if metrics.get("disk_iops", 0) > 5000:
        bottlenecks.append("🔴 磁盘瓶颈: IOPS过高")
    
    # Network bottleneck
    if metrics.get("network_usage", 0) > 90:
        bottlenecks.append("🔴 网络瓶颈: 网络带宽使用率超过90%")
    if metrics.get("packet_loss", 0) > 1:
        bottlenecks.append("🔴 网络瓶颈: 网络丢包率过高")
    
    if not bottlenecks:
        print("✅ 未发现明显性能瓶颈")
    else:
        for b in bottlenecks:
            print(b)
    
    return bottlenecks

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python3 bottleneck_analyzer.py <vm_uuid>")
        sys.exit(1)
    analyze_bottlenecks(sys.argv[1])
