#!/usr/bin/env python3
# coding: utf-8
"""
Resource oversell detection tool
"""
import psutil
import libvirt

def detect_resource_oversell():
    """Detect CPU and memory oversell ratio"""
    conn = libvirt.open('qemu:///system')
    if not conn:
        print("❌ Failed to connect to libvirt")
        return
    
    print("=" * 80)
    print("📊 Resource oversubscription check")
    print("=" * 80)
    
    # Host resources
    host_cpu = psutil.cpu_count()
    host_memory = psutil.virtual_memory().total // 1024**3  # GB
    
    # Allocated resources
    total_vcpus = 0
    total_memory = 0
    running_vms = 0
    
    domains = conn.listAllDomains()
    for domain in domains:
        if domain.isActive():
            running_vms += 1
            vcpus = domain.maxVcpus()
            total_vcpus += vcpus
            mem = domain.maxMemory() // 1024**2  # GB
            total_memory += mem
    
    # Calculate ratios
    cpu_oversell = total_vcpus / host_cpu if host_cpu > 0 else 0
    mem_oversell = total_memory / host_memory if host_memory > 0 else 0
    
    print(f"🖥️  host资源: {host_cpu} vCPU, {host_memory} GB memory")
    print(f"🖥️  已分配资源: {total_vcpus} vCPU, {total_memory} GB memory")
    print(f"📈 CPU超卖率: {cpu_oversell:.2f}x")
    print(f"📈 memory超卖率: {mem_oversell:.2f}x")
    print()
    
    if cpu_oversell > 2.0:
        print("⚠️  Warning: CPU超卖率过高 (> 2.0x)，可能影响性能")
    if mem_oversell > 1.2:
        print("⚠️  Warning: memory超卖率过高 (> 1.2x)，存在OOM风险")
    
    conn.close()
    return cpu_oversell, mem_oversell

if __name__ == "__main__":
    detect_resource_oversell()
