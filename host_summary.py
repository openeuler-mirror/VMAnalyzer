#!/usr/bin/env python3
"""
Host performance summary display
"""
import psutil
import libvirt
from datetime import datetime

def get_host_summary():
    """Get host system performance summary"""
    print("=" * 60)
    print(f"📊 宿主机性能汇总 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # CPU信息
    cpu_count = psutil.cpu_count()
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"💻 CPU: {cpu_count} 核, 使用率: {cpu_usage}%")
    
    # 内存信息
    mem = psutil.virtual_memory()
    print(f"💾 内存: 总 {mem.total//1024**3}GB, 已用 {mem.used//1024**3}GB, 使用率: {mem.percent}%")
    
    # 磁盘信息
    disk = psutil.disk_usage('/')
    print(f"💽 磁盘: 总 {disk.total//1024**3}GB, 已用 {disk.used//1024**3}GB, 使用率: {disk.percent}%")
    
    # 虚拟机数量
    conn = libvirt.open('qemu:///system')
    if conn:
        vms = conn.listAllDomains()
        running_vms = [vm for vm in vms if vm.isActive()]
        print(f"🖥️  虚拟机: 总 {len(vms)} 台, 运行中 {len(running_vms)} 台")
        conn.close()
    
    print("=" * 60)

if __name__ == "__main__":
    get_host_summary()
