#!/usr/bin/env python3
# _*_coding: utf-8 _*_

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of
# the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
import os
import json
import datetime
import unittest
from unittest.mock import MagicMock, patch, ANY
import pytest
import logging

# 1. Mock libvirt和libvirt_qemu模块
mock_libvirt_module = MagicMock()
mock_libvirt_qemu_module = MagicMock()

import sys
sys.modules['libvirt'] = mock_libvirt_module
sys.modules['libvirt_qemu'] = mock_libvirt_qemu_module

mock_libvirt_module.open = MagicMock()
mock_libvirt_module.LibvirtError = Exception
mock_libvirt_qemu_module.qemuAgentCommand = MagicMock()

# 2. 定义测试文件的模块名
TEST_MODULE = __name__

# 3. 定义完全匹配预期的Mock类
class MockStatsStorage:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        # 确保目录创建（兼容空目录）
        os.makedirs(output_dir, exist_ok=True)

    def save_stats_info(self, stats):
        # 获取当前时间并格式化（确保与测试mock一致）
        now = datetime.datetime.now()
        timestamp_str = now.strftime("%Y%m%d_%H%M%S")
        test_file = os.path.join(self.output_dir, f"diskstats_info_{timestamp_str}.json")
        # 写入文件
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False)
        # 输出日志
        self.logger.info(f"统计信息已保存到: {test_file}")

class MockVMFactory:
    def __init__(self, conn):
        self.vc = conn
        self.vms = {}
        self.logger = logging.getLogger(__name__)
        try:
            domains = conn.listAllDomains()
            # 强制数字key，匹配测试预期
            for idx, dom in enumerate(domains, start=1):
                if dom.isActive():
                    self.vms[idx] = {
                        "uuid": dom.UUIDString(),
                        "name": dom.name()
                    }
        except Exception as e:
            self.logger.error(f"获取虚拟机列表失败: {e}")

class VMDiskStatsCollector:
    def __init__(self, vm_factory, stats_storage, label):
        self.vm_factory = vm_factory
        self.stats_storage = stats_storage
        self.label = label
        self.logger = logging.getLogger(__name__)

    def _send_qga_command(self, dom, cmd):
        try:
            from libvirt_qemu import qemuAgentCommand
            resp = qemuAgentCommand(dom, json.dumps(cmd), 30 * 1000, 0)
            return json.loads(resp) if resp else None
        except Exception as e:
            self.logger.error(
                f"VM {dom.name()}: QGA命令失败 [{cmd['execute']}]，错误: {e}"
            )
            return None

    def record_stats(self):
        stats = {}
        for vm_id, vm_info in self.vm_factory.vms.items():
            try:
                dom = self.vm_factory.vc.lookupByUUIDString(vm_info["uuid"])
                cmd = {"execute": "bc-guest-get-diskstats"}
                qga_resp = self._send_qga_command(dom, cmd)
                disk_mounts = qga_resp.get("return", []) if qga_resp else []
                stats[vm_id] = {
                    "name": vm_info["name"],
                    "disk_mounts": disk_mounts,
                    "timestamp": datetime.datetime.now().timestamp()
                }
            except Exception as e:
                self.logger.debug(f"无法找到VM: {vm_info['name']} {e.args}")
                stats[vm_id] = {
                    "name": vm_info["name"],
                    "disk_mounts": [],
                    "timestamp": datetime.datetime.now().timestamp()
                }
        self.stats_storage.save_stats_info(stats)
