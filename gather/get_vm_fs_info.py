#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import libvirt
import json
import logging
import sys
import time
from typing import List, Dict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
LOG_INFO = logging.info
LOG_ERROR = logging.error

class VMAnalyzer:
    def parse_fsinfo(self, raw_fsinfo: List[tuple]) -> List[Dict]:
        parsed_fs_list = []
        for fs in raw_fsinfo:
            volume_name = fs[0] if len(fs) > 0 else "Unknown"
            volume_uuid_path = fs[1] if len(fs) > 1 else ""
            fs_type = fs[2] if len(fs) > 2 else "Unknown"
            device = fs[3][0] if len(fs) > 3 and fs[3] else "Unknown"
            parsed_fs = {
                "volume_name": volume_name,
                "volume_path": volume_uuid_path,
                "fs_type": fs_type,
                "device": device,
                "mount_point": volume_name,
                "is_system_volume": volume_name in ["System Reserved", "C:\\"]
            }
            parsed_fs_list.append(parsed_fs)
        print(parsed_fs_list)
        return parsed_fs_list

    def get_single_vm_info(self, vm_name: str, conn: libvirt.virConnect) -> Dict:
        vm_info = {"uuid": "", "name": vm_name, "status": "", "fs_info": []}
        try:
            LOG_INFO(f"\n===== 开始处理虚拟机：{vm_name} =====")
            dom = conn.lookupByName(vm_name)
            if not dom:
                LOG_ERROR(f"未找到名称为 {vm_name} 的虚拟机")
                vm_info["status"] = "未找到"
                return vm_info

            vm_info["uuid"] = dom.UUIDString()
            vm_state = dom.state()[0]
            state_map = {
                libvirt.VIR_DOMAIN_RUNNING: "运行中",
                libvirt.VIR_DOMAIN_SHUTOFF: "已关闭",
                libvirt.VIR_DOMAIN_PAUSED: "已暂停"
            }
            vm_info["status"] = state_map.get(vm_state, f"未知状态({vm_state})")
            LOG_INFO(f"虚拟机基础信息：名称={vm_name}, UUID={vm_info['uuid']}, 状态={vm_info['status']}")

if __name__ == "__main__":
    main()

