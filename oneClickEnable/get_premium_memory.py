import libvirt
import libvirt_qemu
import json
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
LOG_INFO = logging.info
LOG_ERROR = logging.error

class QgaMemoryStatus:
    def __init__(self):
        self.conn = self._init_libvirt_conn()
        self.domains = {}
        self.QGA_MEMORY_CMD = '{"execute":"guest-get-memory-status"}'

    def _init_libvirt_conn(self) -> libvirt.virConnect:
        try:
            conn = libvirt.open("qemu:///system")
            if conn:
                LOG_INFO("libvirt 连接成功（qemu:///system）")
                return conn
            raise Exception("libvirt 连接失败，未获取到连接句柄")
        except libvirt.libvirtError as e:
            LOG_ERROR(f"libvirt 连接异常：{str(e)}")
            raise

    def get_vm_domain(self, vm_name: str) -> libvirt.virDomain:
        if vm_name in self.domains:
            return self.domains[vm_name]
        
        try:
            dom = self.conn.lookupByName(vm_name)
            self.domains[vm_name] = dom
            LOG_INFO(f"成功获取虚拟机 {vm_name} 句柄")
            return dom
        except libvirt.libvirtError as e:
            LOG_ERROR(f"获取虚拟机 {vm_name} 句柄失败：{str(e)}")
            raise
