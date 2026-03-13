#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
import unittest
import sys
from unittest.mock import patch, MagicMock, mock_open

mock_libvirt = MagicMock()
mock_libvirt.VIR_DOMAIN_RUNNING = 1
mock_libvirt.VIR_DOMAIN_SHUTOFF = 5
mock_libvirt.VIR_DOMAIN_PAUSED = 3
# 定义libvirt异常类，让业务代码能识别
mock_libvirt.libvirtError = type("libvirtError", (Exception,), {"__str__": lambda self: "连接失败"})
sys.modules["libvirt"] = mock_libvirt
sys.modules["gather.get_vm_fs_info.libvirt"] = mock_libvirt

from gather import get_vm_fs_info as vm_fs_info

VIR_DOMAIN_RUNNING = 1
VIR_DOMAIN_SHUTOFF = 5
VIR_DOMAIN_PAUSED = 3

class TestVMAnalyzer(unittest.TestCase):
    """VMAnalyzer类单元测试，覆盖所有核心方法及正常/异常场景"""
    def setUp(self):
        self.analyzer = vm_fs_info.VMAnalyzer()
        self.mock_raw_fsinfo = [
            ("C:\\", "/var/lib/libvirt/images/win10_c.img", "ntfs", ["/dev/vda1"]),
            ("Data", "/var/lib/libvirt/images/win10_data.img", "ntfs", ["/dev/vda2"]),
            ("System Reserved", "/var/lib/libvirt/images/win10_reserved.img", "ntfs", ["/dev/vda3"])
        ]
        self.empty_raw_fsinfo = []
        self.invalid_raw_fsinfo = [("OnlyName",), ("Name&Path", "/path",), (None, None, None)]
        self.mock_vm_name = "test-win10"
        self.mock_vm_uuid = "12345678-1234-1234-1234-1234567890ab"
        self.mock_libvirt_error = mock_libvirt.libvirtError()

    def tearDown(self):
        self.analyzer = None

    def test_parse_fsinfo_normal(self):
        parsed_list = self.analyzer.parse_fsinfo(self.mock_raw_fsinfo)
        self.assertEqual(len(parsed_list), 3)
        c_drive = parsed_list[0]
        self.assertTrue(c_drive["is_system_volume"])
        data_drive = parsed_list[1]
        self.assertFalse(data_drive["is_system_volume"])
        res_drive = parsed_list[2]
        self.assertTrue(res_drive["is_system_volume"])
        self.assertEqual(c_drive["device"], "/dev/vda1")
        self.assertEqual(c_drive["volume_path"], "/var/lib/libvirt/images/win10_c.img")

    def test_parse_fsinfo_empty_and_invalid(self):
        empty_parsed = self.analyzer.parse_fsinfo(self.empty_raw_fsinfo)
        self.assertEqual(len(empty_parsed), 0)
        invalid_parsed = self.analyzer.parse_fsinfo(self.invalid_raw_fsinfo)
        self.assertEqual(len(invalid_parsed), 3)
        self.assertEqual(invalid_parsed[0]["fs_type"], "Unknown")
        self.assertEqual(invalid_parsed[0]["device"], "Unknown")
        self.assertEqual(invalid_parsed[2]["device"], "Unknown")

    @patch.object(vm_fs_info, "LOG_ERROR")
    def test_get_single_vm_info_not_found(self, mock_log_error):
        mock_conn = MagicMock()
        mock_conn.lookupByName.return_value = None
        vm_info = self.analyzer.get_single_vm_info(self.mock_vm_name, mock_conn)
        vm_detail = next(iter(vm_info.values()))
        self.assertIsInstance(vm_detail, str)
        self.assertEqual(vm_detail, "")
        mock_log_error.assert_called_with(f"未找到名称为 {self.mock_vm_name} 的虚拟机")

    @patch.object(vm_fs_info, "LOG_INFO")
    def test_get_single_vm_info_running(self, mock_log_info):
        mock_dom = MagicMock()
        mock_dom.UUIDString.return_value = self.mock_vm_uuid
        mock_dom.state.return_value = (VIR_DOMAIN_RUNNING, 0)
        mock_dom.fsInfo.return_value = self.mock_raw_fsinfo
        mock_conn = MagicMock()
        mock_conn.lookupByName.return_value = mock_dom
        vm_info = self.analyzer.get_single_vm_info(self.mock_vm_name, mock_conn)
        self.assertEqual(vm_info[self.mock_vm_uuid]["status"], "运行中")
        self.assertEqual(len(vm_info[self.mock_vm_uuid]["fs_info"]), 3)
        mock_dom.fsInfo.assert_called_once()
        mock_log_info.assert_any_call(f"{self.mock_vm_name} 文件系统信息获取完成（分区数：3）")

    @patch.object(vm_fs_info, "LOG_INFO")
    def test_get_single_vm_info_shutoff(self, mock_log_info):
        mock_dom = MagicMock()
        mock_dom.UUIDString.return_value = self.mock_vm_uuid
        mock_dom.state.return_value = (VIR_DOMAIN_SHUTOFF, 0)
        mock_conn = MagicMock()
        mock_conn.lookupByName.return_value = mock_dom
        vm_info = self.analyzer.get_single_vm_info(self.mock_vm_name, mock_conn)
        self.assertEqual(vm_info[self.mock_vm_uuid]["status"], "已关闭")
        self.assertEqual(vm_info[self.mock_vm_uuid]["fs_info"], [])
        mock_dom.fsInfo.assert_not_called()
        mock_log_info.assert_any_call(f"{self.mock_vm_name} 非运行状态，跳过文件系统信息获取")

    @patch.object(vm_fs_info, "LOG_ERROR")
    def test_get_single_vm_info_libvirt_error(self, mock_log_error):
        mock_conn = MagicMock()
        mock_conn.lookupByName.side_effect = self.mock_libvirt_error
        vm_info = self.analyzer.get_single_vm_info(self.mock_vm_name, mock_conn)
        vm_detail = next(iter(vm_info.values()))
        self.assertIsInstance(vm_detail, dict)
        self.assertEqual(vm_detail["status"], "异常(连接失败)")
        mock_log_error.assert_called_with(f"{self.mock_vm_name} 信息获取异常：连接失败")

    @patch.object(vm_fs_info, "LOG_INFO")
    def test_get_all_vms_info_no_vms(self, mock_log_info):
        mock_conn = MagicMock()
        mock_conn.listAllDomains.return_value = []
        with patch("gather.get_vm_fs_info.libvirt.open", return_value=mock_conn):
            all_vms = self.analyzer.get_all_vms_info()
            self.assertEqual(all_vms, {})
            mock_log_info.assert_any_call("未找到任何虚拟机")
            mock_conn.close.assert_called_once()

    @patch.object(vm_fs_info, "LOG_INFO")
    def test_get_all_vms_info_normal(self, mock_log_info):
        vm1_name = "test-win10-01"
        vm2_name = "test-centos-01"
        mock_dom1 = MagicMock()
        mock_dom1.name.return_value = vm1_name
        mock_dom2 = MagicMock()
        mock_dom2.name.return_value = vm2_name
        mock_conn = MagicMock()
        mock_conn.listAllDomains.return_value = [mock_dom1, mock_dom2]
        mock_vm1_info = {self.mock_vm_uuid: {"uuid": self.mock_vm_uuid, "name": vm1_name, "status": "运行中"}}
        mock_vm2_info = {"87654321-4321-4321-4321-ba0987654321": {"uuid": "87654321", "name": vm2_name, "status": "已关闭"}}
        with patch("gather.get_vm_fs_info.libvirt.open", return_value=mock_conn), \
             patch.object(self.analyzer, "get_single_vm_info", side_effect=[mock_vm1_info, mock_vm2_info]):
            all_vms = self.analyzer.get_all_vms_info()
            self.assertEqual(len(all_vms), 2)
            self.assertIn(self.mock_vm_uuid, all_vms)
            mock_log_info.assert_any_call(f"共找到 2 台虚拟机：['{vm1_name}', '{vm2_name}']")
            mock_conn.close.assert_called_once()

    @patch.object(vm_fs_info, "LOG_INFO")
    def test_save_to_json_specify_path(self, mock_log_info):
        mock_data = {self.mock_vm_uuid: {"name": self.mock_vm_name, "status": "运行中"}}
        test_file = "test_vm_fs_info.json"
        with patch("builtins.open", mock_open()) as mock_file, \
             patch("gather.get_vm_fs_info.json.dump") as mock_json_dump:
            res_path = self.analyzer.save_to_json(mock_data, test_file)
            self.assertEqual(res_path, test_file)
            mock_file.assert_called_once_with(test_file, "w", encoding="utf-8")
            mock_json_dump.assert_called_once_with(mock_data, mock_file(), indent=2, ensure_ascii=False)
            mock_log_info.assert_called_with(f"所有虚拟机文件系统信息已保存到文件：{test_file}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
