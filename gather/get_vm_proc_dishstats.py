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
            logger.error(f"获取VM列表失败: {e}")
        return vms


class MockStatsStorage:
    def __init__(self, output_dir='/var/lib/vm_diskstats'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def save_stats_info(self, stats_info):
        try:
            if not stats_info:
                logger.warning("Operation message")

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(self.output_dir, f'diskstats_info_{timestamp}.json')
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(stats_info, f, ensure_ascii=False, indent=2)
            logger.info(f"统计信息已保存到: {filename}")
        except Exception as e:
            logger.error(f"保存统计信息失败: {e}")


class VMDiskStatsCollector:
    def __init__(self, vm_factory, stats_storage, label):
        self.__vm_factory = vm_factory
        self.__stats_storage = stats_storage
        self.__label = label

    def _send_qga_command(self, dom, cmd_dict):
        try:
            cmd_json = json.dumps(cmd_dict)
            result = libvirt_qemu.qemuAgentCommand(dom, cmd_json, 30 * 1000, 0)
            return json.loads(result) if result else None
        except Exception as e:
            cmd_type = cmd_dict.get('execute', 'unknown')
            logger.error(f"VM {dom.name()}: QGA命令失败 [{cmd_type}]，Error: {e}")
            return None

    def record_stats(self):
        vm_factory = self.__vm_factory
        label = self.__label
        stats_storage = self.__stats_storage

        if vm_factory is None:
            logger.error("VMFactoryuninitialized")
            return

        vc = vm_factory.vc
        stats_info = {}

        for vm_id, vm in list(vm_factory.vms.items()):
            try:
                dom = vc.lookupByUUIDString(vm['uuid'])
            except Exception as err:
                logger.debug(f"无法找到VM: {vm['name']} {err.args}")
                continue
            timestamp = int(datetime.now().timestamp())

            if label == 'diskStats':
                disk_stats = {
                    'uuid': vm['uuid'],
                    'name': vm['name'],
                    'disk_mounts': [],
                    'timestamp': timestamp
                }

                diskstats_cmd = {
                    "execute": "bc-guest-get-diskstats"
                }
                diskstats_result = self._send_qga_command(dom, diskstats_cmd)
                if diskstats_result and "return" in diskstats_result:
                    disk_stats['disk_mounts'] = diskstats_result["return"]

                stats_info[vm_id] = disk_stats
            else:
                logger.error(f"未知的标签: {label}")

        stats_storage.save_stats_info(stats_info)


def main():
    try:
        conn = libvirt.open('qemu:///system')
        if conn is None:
            logger.error("Operation message")
            return

        vm_factory = MockVMFactory(conn)
        stats_storage = MockStatsStorage()
        collector = VMDiskStatsCollector(vm_factory, stats_storage, 'diskStats')

        collector.record_stats()

        conn.close()
        logger.info("Operation message")

    except Exception as e:
        logger.error(f"主函数执行失败: {e}")


if __name__ == "__main__":
    main()

