#!/usr/bin/env python3
# coding: utf-8
"""
VM snapshot monitoring
"""
import libvirt
from datetime import datetime

def list_vm_snapshots():
    """List all snapshots for all VMs"""
    conn = libvirt.open('qemu:///system')
    if not conn:
        print("❌ 无法连接到libvirt")
        return
    
    print("=" * 80)
    print(f"📸 虚拟机快照列表 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    domains = conn.listAllDomains()
    for domain in domains:
        snapshots = domain.snapshotListNames()
        if snapshots:
            print(f"\n🖥️  虚拟机: {domain.name()} ({domain.UUIDString()})")
            for snap in snapshots:
                print(f"   • {snap}")
    
    conn.close()

if __name__ == "__main__":
    list_vm_snapshots()
