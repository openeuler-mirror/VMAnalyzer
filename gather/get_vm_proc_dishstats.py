#!/usr/bin/env python
# -*- coding: utf-8 -*-

import libvirt
import libvirt_qemu
import json
import logging
import os
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/vm_diskstats_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MockVMFactory:
    def __init__(self, conn):
        self.vc = conn
        self.vms = self._get_all_vms()

    def _get_all_vms(self):
        vms = {}
        try:
            domains = self.vc.listAllDomains()
            for dom in domains:
                if dom.isActive():
                    vm_id = dom.ID()
                    vms[vm_id] = {
                        'uuid': dom.UUIDString(),
                        'name': dom.name()
                    }
        except Exception as e:
            logger.error(f"获取虚拟机列表失败: {e}")
        return vms


if __name__ == "__main__":
    main()

