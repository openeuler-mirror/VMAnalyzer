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

# 业务代码用到的状态常量
VIR_DOMAIN_RUNNING = 1
VIR_DOMAIN_SHUTOFF = 5
VIR_DOMAIN_PAUSED = 3


class TestVMAnalyzer(unittest.TestCase):
    """VMAnalyzer类单元测试，覆盖所有核心方法及正常/异常场景"""

    def setUp(self):
        """测试前置：创建实例+定义通用模拟数据+模拟libvirt异常"""
        self.analyzer = vm_fs_info.VMAnalyzer()
        # 模拟原始fsInfo数据
        self.mock_raw_fsinfo = [
            ("C:\\", "/var/lib/libvirt/images/win10_c.img", "ntfs", ["/dev/vda1"]),
            ("Data", "/var/lib/libvirt/images/win10_data.img", "ntfs", ["/dev/vda2"]),
            ("System Reserved", "/var/lib/libvirt/images/win10_reserved.img", "ntfs", ["/dev/vda3"])
        ]
        self.empty_raw_fsinfo = []
        self.invalid_raw_fsinfo = [("OnlyName",), ("Name&Path", "/path",), (None, None, None)]
        # 通用虚拟机名称/UUID
        self.mock_vm_name = "test-win10"
        self.mock_vm_uuid = "12345678-1234-1234-1234-1234567890ab"
        # 创建业务代码可识别的libvirt异常实例
        self.mock_libvirt_error = mock_libvirt.libvirtError()

    def tearDown(self):
        """测试后置：重置实例"""
        self.analyzer = None

    def test_parse_fsinfo_normal(self):
        """测试parse_fsinfo：正常原始数据解析场景"""
        parsed_list = self.analyzer.parse_fsinfo(self.mock_raw_fsinfo)
        self.assertEqual(len(parsed_list), 3)
        # 断言系统卷/非系统卷判断正确
        c_drive = parsed_list[0]
        self.assertTrue(c_drive["is_system_volume"])
        data_drive = parsed_list[1]
        self.assertFalse(data_drive["is_system_volume"])
        res_drive = parsed_list[2]
        self.assertTrue(res_drive["is_system_volume"])
        # 断言字段解析正确
        self.assertEqual(c_drive["device"], "/dev/vda1")
        self.assertEqual(c_drive["volume_path"], "/var/lib/libvirt/images/win10_c.img")

    def test_parse_fsinfo_empty_and_invalid(self):
        """测试parse_fsinfo：空数据/字段不全的边界场景"""
        # 空数据
        empty_parsed = self.analyzer.parse_fsinfo(self.empty_raw_fsinfo)
        self.assertEqual(len(empty_parsed), 0)
        # 字段不全数据
        invalid_parsed = self.analyzer.parse_fsinfo(self.invalid_raw_fsinfo)
        self.assertEqual(len(invalid_parsed), 3)
        # 断言默认值填充
        self.assertEqual(invalid_parsed[0]["fs_type"], "Unknown")
        self.assertEqual(invalid_parsed[0]["device"], "Unknown")
        self.assertEqual(invalid_parsed[2]["device"], "Unknown")

    @patch.object(vm_fs_info, "LOG_ERROR")
    def test_get_single_vm_info_not_found(self, mock_log_error):
        """测试get_single_vm_info：未找到指定虚拟机场景"""
        mock_conn = MagicMock()
        mock_conn.lookupByName.return_value = None
        vm_info = self.analyzer.get_single_vm_info(self.mock_vm_name, mock_conn)
        vm_detail = next(iter(vm_info.values()))
        self.assertIsInstance(vm_detail, str)
        self.assertEqual(vm_detail, "")
        mock_log_error.assert_called_with(f"未找到名称为 {self.mock_vm_name} 的虚拟机")

    @patch.object(vm_fs_info, "LOG_INFO")
    def test_get_single_vm_info_running(self, mock_log_info):
        """测试get_single_vm_info：虚拟机运行中（正常获取fsInfo）场景"""
        mock_dom = MagicMock()
        mock_dom.UUIDString.return_value = self.mock_vm_uuid
        mock_dom.state.return_value = (VIR_DOMAIN_RUNNING, 0)
        mock_dom.fsInfo.return_value = self.mock_raw_fsinfo
        # Mock连接对象
        mock_conn = MagicMock()
        mock_conn.lookupByName.return_value = mock_dom
        # 调用方法
        vm_info = self.analyzer.get_single_vm_info(self.mock_vm_name, mock_conn)
        # 断言
        self.assertEqual(vm_info[self.mock_vm_uuid]["status"], "运行中")
        self.assertEqual(len(vm_info[self.mock_vm_uuid]["fs_info"]), 3)
        mock_dom.fsInfo.assert_called_once()
        mock_log_info.assert_any_call(f"{self.mock_vm_name} 文件系统信息获取完成（分区数：3）")

    @patch.object(vm_fs_info, "LOG_INFO")
    def test_get_single_vm_info_shutoff(self, mock_log_info):
        """测试get_single_vm_info：虚拟机已关闭（跳过fsInfo）场景"""
        mock_dom = MagicMock()
        mock_dom.UUIDString.return_value = self.mock_vm_uuid
        mock_dom.state.return_value = (VIR_DOMAIN_SHUTOFF, 0)
        mock_conn = MagicMock()
        mock_conn.lookupByName.return_value = mock_dom
        # 调用
        vm_info = self.analyzer.get_single_vm_info(self.mock_vm_name, mock_conn)
        # 断言
        self.assertEqual(vm_info[self.mock_vm_uuid]["status"], "已关闭")
        self.assertEqual(vm_info[self.mock_vm_uuid]["fs_info"], [])
        mock_dom.fsInfo.assert_not_called()
        mock_log_info.assert_any_call(f"{self.mock_vm_name} 非运行状态，跳过文件系统信息获取")

    @patch.object(vm_fs_info, "LOG_ERROR")
    def test_get_single_vm_info_libvirt_error(self, mock_log_error):
        """测试get_single_vm_info：抛出libvirtError异常场景"""
        mock_conn = MagicMock()
        # 抛出业务代码可识别的libvirt异常
        mock_conn.lookupByName.side_effect = self.mock_libvirt_error
        # 调用方法
        vm_info = self.analyzer.get_single_vm_info(self.mock_vm_name, mock_conn)
        # 异常处理后value是字典，正常断言status
        vm_detail = next(iter(vm_info.values()))
        self.assertIsInstance(vm_detail, dict)
        self.assertEqual(vm_detail["status"], "异常(连接失败)")
        # 核心断言：错误日志已正确调用
        mock_log_error.assert_called_with(f"{self.mock_vm_name} 信息获取异常：连接失败")

    @patch.object(vm_fs_info, "LOG_ERROR")
    def test_get_all_vms_info_connect_failed(self, mock_log_error):
        """测试get_all_vms_info：libvirt服务连接失败场景"""
        with patch("gather.get_vm_fs_info.libvirt.open", return_value=None):
            all_vms = self.analyzer.get_all_vms_info()
            self.assertEqual(all_vms, {})
            mock_log_error.assert_called_with("连接 libvirt 服务失败！请检查 libvirtd 服务是否启动及权限是否足够")

    @patch.object(vm_fs_info, "LOG_INFO")
    def test_get_all_vms_info_no_vms(self, mock_log_info):
        """测试get_all_vms_info：连接成功但无虚拟机场景"""
        mock_conn = MagicMock()
        mock_conn.listAllDomains.return_value = []
        with patch("gather.get_vm_fs_info.libvirt.open", return_value=mock_conn):
            all_vms = self.analyzer.get_all_vms_info()
            self.assertEqual(all_vms, {})
            mock_log_info.assert_any_call("未找到任何虚拟机")
            mock_conn.close.assert_called_once()

    @patch.object(vm_fs_info, "LOG_INFO")
    def test_get_all_vms_info_normal(self, mock_log_info):
        """测试get_all_vms_info：连接成功且有多个虚拟机场景"""
        # 模拟两个虚拟机
        vm1_name = "test-win10-01"
        vm2_name = "test-centos-01"
        mock_dom1 = MagicMock()
        mock_dom1.name.return_value = vm1_name
        mock_dom2 = MagicMock()
        mock_dom2.name.return_value = vm2_name
        # Mock连接
        mock_conn = MagicMock()
        mock_conn.listAllDomains.return_value = [mock_dom1, mock_dom2]
        # Mock单虚拟机信息返回
        mock_vm1_info = {self.mock_vm_uuid: {"uuid": self.mock_vm_uuid, "name": vm1_name, "status": "运行中"}}
        mock_vm2_info = {"87654321-4321-4321-4321-ba0987654321": {"uuid": "87654321", "name": vm2_name, "status": "已关闭"}}
        # 嵌套Mock
        with patch("gather.get_vm_fs_info.libvirt.open", return_value=mock_conn), \
             patch.object(self.analyzer, "get_single_vm_info", side_effect=[mock_vm1_info, mock_vm2_info]):
            all_vms = self.analyzer.get_all_vms_info()
            # 断言
            self.assertEqual(len(all_vms), 2)
            self.assertIn(self.mock_vm_uuid, all_vms)
            # 日志字符串匹配业务代码实际输出（单引号包裹）
            mock_log_info.assert_any_call(f"共找到 2 台虚拟机：['{vm1_name}', '{vm2_name}']")
            mock_conn.close.assert_called_once()

    @patch.object(vm_fs_info, "LOG_INFO")
    def test_save_to_json_specify_path(self, mock_log_info):
        """测试save_to_json：指定文件路径场景"""
        mock_data = {self.mock_vm_uuid: {"name": self.mock_vm_name, "status": "运行中"}}
        test_file = "test_vm_fs_info.json"
        with patch("builtins.open", mock_open()) as mock_file, \
             patch("gather.get_vm_fs_info.json.dump") as mock_json_dump:
            res_path = self.analyzer.save_to_json(mock_data, test_file)
            self.assertEqual(res_path, test_file)
            mock_file.assert_called_once_with(test_file, "w", encoding="utf-8")
            mock_json_dump.assert_called_once_with(mock_data, mock_file(), indent=2, ensure_ascii=False)
            mock_log_info.assert_called_with(f"所有虚拟机文件系统信息已保存到文件：{test_file}")

    @patch.object(vm_fs_info, "LOG_INFO")
    def test_save_to_json_default_path(self, mock_log_info):
        """测试save_to_json：使用默认时间戳文件路径场景"""
        mock_data = {self.mock_vm_uuid: {"name": self.mock_vm_name, "status": "运行中"}}
        with patch("builtins.open", mock_open()) as mock_default_file, \
             patch("gather.get_vm_fs_info.json.dump"):
            res_path = self.analyzer.save_to_json(mock_data)
            self.assertIn("vm_fs_info_all_", res_path)
            mock_default_file.assert_called_once_with(res_path, "w", encoding="utf-8")
            mock_log_info.assert_called_with(f"所有虚拟机文件系统信息已保存到文件：{res_path}")


if __name__ == "__main__":
    unittest.main(verbosity=2)

