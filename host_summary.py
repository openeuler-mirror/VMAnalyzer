#!/usr/bin/env python3
# coding: utf-8
"""
Host performance summary display
"""
import psutil
import libvirt
from datetime import datetime

def get_host_summary():
    """Get host system performance summary"""
    print("=" * 60)
    print(f"📊 host性能汇总 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # English comment for this block.
    cpu_count = psutil.cpu_count()
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"💻 CPU: {cpu_count} 核, 使用率: {cpu_usage}%")
    
    # English comment for this block.
    mem = psutil.virtual_memory()
    print(f"💾 memory: 总 {mem.total//1024**3}GB, 已用 {mem.used//1024**3}GB, 使用率: {mem.percent}%")
    
    # English comment for this block.
    disk = psutil.disk_usage('/')
    print(f"💽 disk: 总 {disk.total//1024**3}GB, 已用 {disk.used//1024**3}GB, 使用率: {disk.percent}%")
    
    # English comment for this block.
    conn = libvirt.open('qemu:///system')
    if conn:
        vms = conn.listAllDomains()
        running_vms = [vm for vm in vms if vm.isActive()]
        print(f"🖥️  VM: 总 {len(vms)} 台, running {len(running_vms)} 台")
        conn.close()
    
    print("=" * 60)

if __name__ == "__main__":
    get_host_summary()
