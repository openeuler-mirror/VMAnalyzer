#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import json
import os
from unittest.mock import patch, MagicMock

try:
    from gather.get_vm_disk_status import VMCollector
except ImportError:
    import sys
    sys.path.insert(0, '../../..')
    from gather.get_vm_disk_status import VMCollector


class TestVMDiskStatusCollector(unittest.TestCase):
    """测试虚拟机磁盘状态采集模块"""

    def setUp(self):
        """初始化测试环境"""
        self.collector = VMCollector(output_dir="/tmp/test_disk_status")

    def tearDown(self):
        """清理测试环境"""
        import shutil
        if os.path.exists("/tmp/test_disk_status"):
            shutil.rmtree("/tmp/test_disk_status")

    @patch('gather.get_vm_disk_status.subprocess.run')
    def test_run_virsh_cmd_success(self, mock_run):
        """测试执行virsh命令成功"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout.strip.return_value = "output"
        mock_run.return_value = mock_result

        result = self.collector.run_virsh_cmd("virsh list")
        self.assertEqual(result, "output")

    @patch('gather.get_vm_disk_status.subprocess.run')
    def test_run_virsh_cmd_timeout(self, mock_run):
        """测试命令执行超时"""
        from subprocess import TimeoutExpired
        mock_run.side_effect = TimeoutExpired("cmd", 30)
        
        result = self.collector.run_virsh_cmd("sleep 60")
        self.assertIsNone(result)

    @patch('gather.get_vm_disk_status.VMCollector.run_virsh_cmd')
    def test_get_vm_state(self, mock_run):
        """测试获取虚拟机状态"""
        mock_run.return_value = "running"
        
        state = self.collector.get_vm_state("test-vm")
        self.assertEqual(state, "running")

    @patch('gather.get_vm_disk_status.VMCollector.run_virsh_cmd')
    def test_call_qga_interface_success(self, mock_run):
        """测试调用QGA接口成功"""
        mock_run.return_value = json.dumps({
            "return": [
                {"device": "/dev/sda", "status": "ok"}
            ]
        })
        
        result = self.collector.call_qga_interface("test-vm", "guest-get-disk-status")
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["data"]), 1)

    @patch('gather.get_vm_disk_status.VMCollector.run_virsh_cmd')
    def test_call_qga_interface_not_running(self, mock_run):
        """测试对非运行虚拟机调用QGA接口"""
        mock_run.return_value = "shut off"
        
        result = self.collector.call_qga_interface("test-vm", "guest-get-disk-status")
        
        self.assertEqual(result["status"], "failed")
        self.assertIn("无法调用QGA接口", result["error"])

    @patch('gather.get_vm_disk_status.VMCollector.run_virsh_cmd')
    def test_collect_single_vm_data(self, mock_run):
        """测试采集单个虚拟机磁盘数据"""
        mock_run.side_effect = [
            "running",  # get_vm_state
            json.dumps({"return": [{"device": "/dev/sda", "status": "ok"}]})  # call_qga_interface
        ]
        
        data = self.collector.collect_single_vm_data("test-vm")
        
        self.assertEqual(data["name"], "test-vm")
        self.assertEqual(data["state"], "running")
        self.assertEqual(data["get_disk_status"]["data"][0]["device"], "/dev/sda")

    @patch('gather.get_vm_disk_status.VMCollector.collect_single_vm_data')
    @patch('gather.get_vm_disk_status.VMCollector.get_all_vm_names')
    def test_collect_all_vms(self, mock_get_names, mock_collect_single):
        """测试采集所有虚拟机数据"""
        mock_get_names.return_value = ["vm1", "vm2"]
        mock_collect_single.return_value = {"name": "vm1", "state": "running"}
        
        self.collector.collect_all_vms()
        
        self.assertEqual(self.collector.all_vms_data["vm_count"], 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
