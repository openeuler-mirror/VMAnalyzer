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

            if vm_state == libvirt.VIR_DOMAIN_RUNNING:
                LOG_INFO(f"正在获取 {vm_name} 文件系统信息...")
                raw_fsinfo = dom.fsInfo()
                parsed_fs = self.parse_fsinfo(raw_fsinfo)
                vm_info["fs_info"] = parsed_fs
                LOG_INFO(f"{vm_name} 文件系统信息获取完成（分区数：{len(parsed_fs)}）")
            else:
                LOG_INFO(f"{vm_name} 非运行状态，跳过文件系统信息获取")

        except libvirt.libvirtError as e:
            LOG_ERROR(f"{vm_name} 信息获取异常：{str(e)}")
            vm_info["status"] = f"异常({str(e)})"
        except Exception as e:
            LOG_ERROR(f"{vm_name} 处理失败：{str(e)}")
            vm_info["status"] = f"处理失败({str(e)})"
        return {vm_info["uuid"]: vm_info}

    def get_all_vms_info(self) -> Dict:
        conn = None
        all_vms_info = {}
        try:
            LOG_INFO("正在连接 libvirt 服务...")
            conn = libvirt.open("qemu:///system")
            if not conn:
                LOG_ERROR("连接 libvirt 服务失败！请检查 libvirtd 服务是否启动及权限是否足够")
                return all_vms_info

            LOG_INFO("正在获取所有虚拟机列表...")
            domains = conn.listAllDomains()
            vm_names = [dom.name() for dom in domains]
            if not vm_names:
                LOG_INFO("未找到任何虚拟机")
                return all_vms_info
            LOG_INFO(f"共找到 {len(vm_names)} 台虚拟机：{vm_names}")

            for vm_name in vm_names:
                single_vm_info = self.get_single_vm_info(vm_name, conn)
                all_vms_info.update(single_vm_info)

        except libvirt.libvirtError as e:
            LOG_ERROR(f"程序执行异常：{str(e)}")
        finally:
            if conn:
                conn.close()
                LOG_INFO("libvirt 连接已关闭")
        return all_vms_info

    def save_to_json(self, all_vms_info: Dict, file_path: str = None):
        if not file_path:
            file_path = f"vm_fs_info_all_{int(time.time())}.json"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(all_vms_info, f, indent=2, ensure_ascii=False)
            LOG_INFO(f"所有虚拟机文件系统信息已保存到文件：{file_path}")
            return file_path
        except Exception as e:
            LOG_ERROR(f"保存JSON文件失败：{str(e)}")
            raise

def main():
    if len(sys.argv) != 1:
        print("Usage: python3 vm_fs_info_all.py")
        print("示例：python3 vm_fs_info_all.py")
        sys.exit(1)

    analyzer = VMAnalyzer()
    all_vms_info = analyzer.get_all_vms_info()

    if all_vms_info:
        LOG_INFO(f"\n===== 所有虚拟机信息检测完成，共处理 {len(all_vms_info)} 台虚拟机 =====")
        filename = analyzer.save_to_json(all_vms_info)
        
        print("\n===== 简要统计 =====")
        for vm_uuid, info in all_vms_info.items():
            print(f"虚拟机：{info['name']}（{info['status']}）- 分区数：{len(info['fs_info'])}")
    else:
        LOG_ERROR("未获取到任何虚拟机信息")
        sys.exit(1)

if __name__ == "__main__":
    main()

