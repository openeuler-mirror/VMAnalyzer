#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import json
import os
from unittest.mock import patch, MagicMock

try:
    from gather.get_vm_cpu_utilization import VMCollector
except ImportError:
    import sys
    sys.path.insert(0, '../../..')
    from gather.get_vm_cpu_utilization import VMCollector


class TestVMCPUUtilizationCollector(unittest.TestCase):
    """测试虚拟机CPU利用率采集模块"""

    def setUp(self):
        """初始化测试环境"""
        self.collector = VMCollector(output_dir="/tmp/test_cpu_util")

    def tearDown(self):
        """清理测试环境"""
        import shutil
        if os.path.exists("/tmp/test_cpu_util"):
            shutil.rmtree("/tmp/test_cpu_util")

    @patch('gather.get_vm_cpu_utilization.subprocess.run')
    def test_run_virsh_cmd_success(self, mock_run):
        """测试执行virsh命令成功"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout.strip.return_value = "output"
        mock_run.return_value = mock_result

        result = self.collector.run_virsh_cmd("virsh list")
        self.assertEqual(result, "output")

    @patch('gather.get_vm_cpu_utilization.subprocess.run')
    def test_run_virsh_cmd_failed(self, mock_run):
        """测试执行virsh命令失败"""
        mock_run.side_effect = Exception("command error")
        
        result = self.collector.run_virsh_cmd("invalid command")
        self.assertIsNone(result)

    @patch('gather.get_vm_cpu_utilization.VMCollector.run_virsh_cmd')
    def test_get_all_vm_names(self, mock_run):
        """测试获取虚拟机名称列表"""
        mock_run.return_value = "vm1 vm2 vm3"
        
        vms = self.collector.get_all_vm_names()
        self.assertEqual(vms, ["vm1", "vm2", "vm3"])

    @patch('gather.get_vm_cpu_utilization.VMCollector.run_virsh_cmd')
    def test_get_vm_state(self, mock_run):
        """测试获取虚拟机状态"""
        mock_run.return_value = "running"
        
        state = self.collector.get_vm_state("test-vm")
        self.assertEqual(state, "running")

    @patch('gather.get_vm_cpu_utilization.VMCollector.run_virsh_cmd')
    def test_call_qga_interface_success(self, mock_run):
        """测试调用QGA接口成功"""
        mock_run.return_value = json.dumps({"return": {"cpu": 10.5}})
        
        result = self.collector.call_qga_interface("test-vm", "guest-get-cpu-utilization")
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"], {"cpu": 10.5})

    @patch('gather.get_vm_cpu_utilization.VMCollector.run_virsh_cmd')
    def test_call_qga_interface_failed(self, mock_run):
        """测试调用QGA接口失败"""
        mock_run.return_value = json.dumps({"error": {"message": "failed"}})
        
        result = self.collector.call_qga_interface("test-vm", "guest-get-cpu-utilization")
        
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["error"], "failed")

    @patch('gather.get_vm_cpu_utilization.VMCollector.run_virsh_cmd')
    def test_collect_single_vm_data(self, mock_run):
        """测试采集单个虚拟机数据"""
        mock_run.side_effect = [
            "running",  # get_vm_state
            json.dumps({"return": {"cpu": 25.5}})  # call_qga_interface
        ]
        
        data = self.collector.collect_single_vm_data("test-vm")
        
        self.assertEqual(data["name"], "test-vm")
        self.assertEqual(data["state"], "running")
        self.assertEqual(data["get_cpu_utilization"]["data"], {"cpu": 25.5})

    @patch('gather.get_vm_cpu_utilization.VMCollector.run_virsh_cmd')
    def test_collect_single_vm_data_not_running(self, mock_run):
        """测试采集非运行状态虚拟机数据"""
        mock_run.return_value = "shut off"
        
        data = self.collector.collect_single_vm_data("test-vm")
        
        self.assertEqual(data["state"], "shut off")
        self.assertIn("跳过QGA调用", data["get_cpu_utilization"]["error"])


if __name__ == '__main__':
    unittest.main(verbosity=2)
