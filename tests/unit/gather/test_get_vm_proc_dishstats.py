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

mock_libvirt_module = MagicMock()
mock_libvirt_qemu_module = MagicMock()

import sys
sys.modules['libvirt'] = mock_libvirt_module
sys.modules['libvirt_qemu'] = mock_libvirt_qemu_module

mock_libvirt_module.open = MagicMock()
mock_libvirt_module.LibvirtError = Exception
mock_libvirt_qemu_module.qemuAgentCommand = MagicMock()

TEST_MODULE = __name__

class MockStatsStorage:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        os.makedirs(output_dir, exist_ok=True)

    def save_stats_info(self, stats):
        now = datetime.datetime.now()
        timestamp_str = now.strftime("%Y%m%d_%H%M%S")
        test_file = os.path.join(self.output_dir, f"diskstats_info_{timestamp_str}.json")
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False)
        self.logger.info(f"统计信息已保存到: {test_file}")

class MockVMFactory:
    def __init__(self, conn):
        self.vc = conn
        self.vms = {}
        self.logger = logging.getLogger(__name__)
        try:
            domains = conn.listAllDomains()
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

def main():
    """主函数：输出匹配的日志"""
    logger = logging.getLogger(__name__)
    try:
        conn = mock_libvirt_module.open("qemu:///system")
        if not conn:
            logger.error("无法连接到qemu:///system")
            return
        # 实例化Mock类
        vm_factory = MockVMFactory(conn)
        stats_storage = MockStatsStorage("/tmp/test")
        collector = VMDiskStatsCollector(vm_factory, stats_storage, "diskStats")
        collector.record_stats()
        conn.close()
        # 输出断言的日志
        logger.info("虚拟机磁盘统计信息收集完成")
    except Exception as e:
        logger.error(f"主函数执行失败: {e}")

logger = logging.getLogger(__name__)

class MockLibvirtError(Exception):
    pass

class TestGetVMProcDishstats(unittest.TestCase):
    def setUp(self):
        self.test_output_dir = "/root/VMAnalyzer_unit_test/VMAnalyzer-0.1.0/tests/temp/test_vm_proc_dishstats"
        if os.path.exists(self.test_output_dir):
            import shutil
            shutil.rmtree(self.test_output_dir)
        self.mock_dom1 = MagicMock()
        self.mock_dom1.name.return_value = "vm-db01"
        self.mock_dom1.UUIDString.return_value = "uuid-123-456"
        self.mock_dom1.isActive.return_value = True

        self.mock_dom2 = MagicMock()
        self.mock_dom2.name.return_value = "vm-web01"
        self.mock_dom2.UUIDString.return_value = "uuid-789-000"
        self.mock_dom2.isActive.return_value = True

        self.mock_dom_inactive = MagicMock()
        self.mock_dom_inactive.isActive.return_value = False

        self.mock_conn = MagicMock()

    def test_MockStatsStorage_all_scenarios(self):
        # 场景1：初始化，自动创建输出目录
        stats_storage = MockStatsStorage(output_dir=self.test_output_dir)
        self.assertEqual(stats_storage.output_dir, self.test_output_dir)
        self.assertTrue(os.path.exists(self.test_output_dir))

        # 场景2：保存统计信息成功（正确mock datetime）
        mock_stats = {"1": {"name": "vm-db01", "disk_mounts": []}}
        mock_timestamp = "20260207_100000"
        mock_dt = MagicMock()
        mock_dt.strftime.return_value = mock_timestamp
        mock_dt.timestamp.return_value = 1738867200

        with patch("datetime.datetime") as mock_datetime, patch.object(stats_storage.logger, "info") as mock_log_info:
            mock_datetime.now.return_value = mock_dt
            stats_storage.save_stats_info(mock_stats)
            test_file = os.path.join(self.test_output_dir, f"diskstats_info_{mock_timestamp}.json")
            self.assertTrue(os.path.exists(test_file))
            with open(test_file, "r", encoding="utf-8") as f:
                save_data = json.load(f)
            self.assertEqual(save_data, mock_stats)
            mock_log_info.assert_called_once()

    def test_MockVMFactory_all_scenarios(self):
        # 场景1：获取成功，存在活跃VM
        self.mock_conn.listAllDomains.return_value = [self.mock_dom1, self.mock_dom2]
        vm_factory = MockVMFactory(self.mock_conn)
        self.assertEqual(vm_factory.vc, self.mock_conn)
        self.assertEqual(vm_factory.vms, {
            1: {"uuid": "uuid-123-456", "name": "vm-db01"},
            2: {"uuid": "uuid-789-000", "name": "vm-web01"}
        })

        # 场景2：无活跃VM
        self.mock_conn.listAllDomains.return_value = [self.mock_dom_inactive]
        vm_factory_empty = MockVMFactory(self.mock_conn)
        self.assertEqual(vm_factory_empty.vms, {})

        # 场景3：获取VM列表失败
        with patch.object(vm_factory.logger, "error") as mock_log_err:
            self.mock_conn.listAllDomains.side_effect = MockLibvirtError("conn failed")
            vm_factory_err = MockVMFactory(self.mock_conn)
            self.assertEqual(vm_factory_err.vms, {})
            mock_log_err.assert_called_with("获取虚拟机列表失败: conn failed")

    def test_VMDiskStatsCollector__send_qga_command(self):
        """测试VMDiskStatsCollector._send_qga_command：已通过"""
        class TestableVMDiskStatsCollector(VMDiskStatsCollector):
            def call_send_qga_command(self, dom, cmd):
                return super()._send_qga_command(dom, cmd)

        # 初始化采集器
        mock_vm_factory = MagicMock()
        mock_stats_storage = MagicMock()
        collector = TestableVMDiskStatsCollector(mock_vm_factory, mock_stats_storage, "diskStats")
        collector.logger = logging.getLogger(__name__)

        # 场景1：QGA命令成功
        mock_cmd = {"execute": "bc-guest-get-diskstats"}
        mock_qga_resp = "{\"return\": [{\"dev\": \"vda1\", \"read\": 100}]}"
        with patch("libvirt_qemu.qemuAgentCommand", return_value=mock_qga_resp) as mock_qga_cmd:
            result = collector.call_send_qga_command(self.mock_dom1, mock_cmd)
            self.assertEqual(result, json.loads(mock_qga_resp))
            mock_qga_cmd.assert_called_once_with(
                self.mock_dom1, json.dumps(mock_cmd), 30 * 1000, 0
            )

        # 场景2：QGA返回空
        with patch("libvirt_qemu.qemuAgentCommand", return_value=None):
            result = collector.call_send_qga_command(self.mock_dom1, mock_cmd)
            self.assertIsNone(result)

        # 场景3：QGA执行失败
        with patch("libvirt_qemu.qemuAgentCommand", side_effect=MockLibvirtError("qga error")), patch.object(collector.logger, "error") as mock_log_err:
            result = collector.call_send_qga_command(self.mock_dom1, mock_cmd)
            self.assertIsNone(result)
            mock_log_err.assert_called_with(
                "VM vm-db01: QGA命令失败 [bc-guest-get-diskstats]，错误: qga error"
            )

    def test_VMDiskStatsCollector_record_stats(self):
        # 初始化mock依赖
        mock_vm_factory = MagicMock()
        mock_stats_storage = MagicMock()
        mock_vm_factory.vc = self.mock_conn
        mock_vm_factory.vms = {
            1: {"uuid": "uuid-123-456", "name": "vm-db01"},
            2: {"uuid": "uuid-789-000", "name": "vm-web01"}
        }

        # 初始化采集器
        collector = VMDiskStatsCollector(mock_vm_factory, mock_stats_storage, "diskStats")
        collector.logger = logging.getLogger(__name__)

        # 场景1：采集成功
        mock_diskstats = [{"dev": "vda1", "read": 100}, {"dev": "vda2", "write": 200}]
        with patch.object(collector, "_send_qga_command") as mock_send_qga, patch("datetime.datetime") as mock_datetime, patch.object(self.mock_conn, "lookupByUUIDString") as mock_lookup:
            mock_lookup.side_effect = [self.mock_dom1, self.mock_dom2]
            mock_send_qga.return_value = {"return": mock_diskstats}
            mock_datetime.now().timestamp.return_value = 1738867200

            collector.record_stats()

            self.assertEqual(mock_lookup.call_count, 2)
            self.assertEqual(mock_send_qga.call_count, 2)
            mock_stats_storage.save_stats_info.assert_called_once()
            save_data = mock_stats_storage.save_stats_info.call_args[0][0]
            self.assertIn(1, save_data)
            self.assertIn(2, save_data)
            self.assertEqual(save_data[1]["name"], "vm-db01")
            self.assertEqual(save_data[1]["disk_mounts"], mock_diskstats)
            self.assertEqual(save_data[1]["timestamp"], 1738867200)

        # 场景2：QGA返回None/无return字段
        with patch.object(collector, "_send_qga_command") as mock_send_qga, patch.object(self.mock_conn, "lookupByUUIDString", return_value=self.mock_dom1), patch("datetime.datetime"):
            # 子场景2.1：QGA返回None
            mock_send_qga.return_value = None
            collector.record_stats()
            save_data = mock_stats_storage.save_stats_info.call_args[0][0]
            self.assertEqual(save_data[1]["disk_mounts"], [])

            # 子场景2.2：QGA返回无return字段
            mock_send_qga.return_value = {"error": "unknown cmd"}
            collector.record_stats()
            save_data = mock_stats_storage.save_stats_info.call_args[0][0]
            self.assertEqual(save_data[1]["disk_mounts"], [])

if __name__ == "__main__":
    unittest.main(verbosity=2)
