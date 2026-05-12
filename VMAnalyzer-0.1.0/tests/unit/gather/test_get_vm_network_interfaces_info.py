#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import json
import os
from unittest.mock import patch, MagicMock

try:
    from gather.get_vm_network_interfaces_info import VMCollector
except ImportError:
    import sys
    sys.path.insert(0, '../../..')
    from gather.get_vm_network_interfaces_info import VMCollector


class TestVMNetworkInterfacesInfo(unittest.TestCase):
    """测试虚拟机网络接口信息采集模块"""

    def setUp(self):
        """初始化测试环境"""
        self.collector = VMCollector(output_dir="/tmp/test_network_info")

    def tearDown(self):
        """清理测试环境"""
        import shutil
        if os.path.exists("/tmp/test_network_info"):
            shutil.rmtree("/tmp/test_network_info")

    @patch('gather.get_vm_network_interfaces_info.subprocess.run')
    def test_run_virsh_cmd_success(self, mock_run):
        """测试执行virsh命令成功"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout.strip.return_value = "output"
        mock_run.return_value = mock_result

        result = self.collector.run_virsh_cmd("virsh list")
        self.assertEqual(result, "output")

    @patch('gather.get_vm_network_interfaces_info.subprocess.run')
    def test_run_virsh_cmd_error(self, mock_run):
        """测试执行virsh命令失败"""
        from subprocess import CalledProcessError
        mock_run.side_effect = CalledProcessError(1, "cmd")
        
        result = self.collector.run_virsh_cmd("invalid command")
        self.assertIsNone(result)

    @patch('gather.get_vm_network_interfaces_info.VMCollector.run_virsh_cmd')
    def test_get_all_vm_names(self, mock_run):
        """测试获取虚拟机名称列表"""
        mock_run.return_value = "vm1 vm2"
        
        vms = self.collector.get_all_vm_names()
        self.assertEqual(vms, ["vm1", "vm2"])

    @patch('gather.get_vm_network_interfaces_info.VMCollector.run_virsh_cmd')
    def test_call_qga_interface_success(self, mock_run):
        """测试调用QGA接口成功"""
        mock_run.return_value = json.dumps({
            "return": [
                {
                    "name": "eth0",
                    "ip-addresses": [{"ip-address": "192.168.1.100"}]
                }
            ]
        })
        
        result = self.collector.call_qga_interface("test-vm", "guest-network-get-interfaces")
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"][0]["name"], "eth0")

    @patch('gather.get_vm_network_interfaces_info.VMCollector.run_virsh_cmd')
    def test_call_qga_interface_parse_error(self, mock_run):
        """测试解析QGA返回结果失败"""
        mock_run.return_value = "invalid json"
        
        result = self.collector.call_qga_interface("test-vm", "guest-network-get-interfaces")
        
        self.assertEqual(result["status"], "parse_error")

    @patch('gather.get_vm_network_interfaces_info.VMCollector.run_virsh_cmd')
    def test_collect_single_vm_networkinfo_data(self, mock_run):
        """测试采集单个虚拟机网络信息"""
        mock_run.return_value = json.dumps({
            "return": [
                {"name": "eth0", "ip-addresses": []}
            ]
        })
        
        data = self.collector.collect_single_vm_networkinfo_data("test-vm")
        
        self.assertEqual(data["name"], "test-vm")
        self.assertEqual(data["get_network_info"]["data"][0]["name"], "eth0")

    @patch('gather.get_vm_network_interfaces_info.VMCollector.collect_single_vm_networkinfo_data')
    @patch('gather.get_vm_network_interfaces_info.VMCollector.get_all_vm_names')
    def test_collect_all_vms_empty(self, mock_get_names, mock_collect_single):
        """测试采集空虚拟机列表"""
        mock_get_names.return_value = []
        
        self.collector.collect_all_vms()
        
        self.assertEqual(self.collector.all_vms_data["vm_count"], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
