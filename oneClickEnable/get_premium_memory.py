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


