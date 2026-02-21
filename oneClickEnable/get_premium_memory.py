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


