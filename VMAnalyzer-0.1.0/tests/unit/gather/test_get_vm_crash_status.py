#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import json
from unittest.mock import patch, MagicMock

try:
    from gather.get_vm_crash_status import execute_cmd, get_vm_list, get_vm_crash_status
except ImportError:
    import sys
    sys.path.insert(0, '../../..')
    from gather.get_vm_crash_status import execute_cmd, get_vm_list, get_vm_crash_status


class TestGetVMCrashStatus(unittest.TestCase):
    """测试虚拟机崩溃状态检测模块"""

    def test_execute_cmd_success(self):
        """测试执行命令成功"""
        result = execute_cmd(["echo", "test"])
        self.assertEqual(result["code"], 0)
        self.assertEqual(result["stdout"], "test")
        self.assertEqual(result["stderr"], "")

    def test_execute_cmd_timeout(self):
        """测试命令执行超时"""
        result = execute_cmd(["sleep", "2"], timeout=1)
        self.assertEqual(result["code"], -1)
        self.assertIn("超时", result["stderr"])

    def test_execute_cmd_error(self):
        """测试命令执行失败"""
        result = execute_cmd(["invalid_command_xyz"])
        self.assertNotEqual(result["code"], 0)

    @patch('gather.get_vm_crash_status.execute_cmd')
    def test_get_vm_list_success(self, mock_exec):
        """测试获取虚拟机列表成功"""
        mock_exec.return_value = {"code": 0, "stdout": "vm1\nvm2\nvm3", "stderr": ""}
        vms = get_vm_list()
        self.assertEqual(vms, ["vm1", "vm2", "vm3"])

    @patch('gather.get_vm_crash_status.execute_cmd')
    def test_get_vm_list_empty(self, mock_exec):
        """测试获取空虚拟机列表"""
        mock_exec.return_value = {"code": 0, "stdout": "", "stderr": ""}
        vms = get_vm_list()
        self.assertEqual(vms, [])

    @patch('gather.get_vm_crash_status.execute_cmd')
    @patch('gather.get_vm_crash_status.os.path.exists')
    def test_get_vm_crash_status_not_crashed(self, mock_exists, mock_exec):
        """测试虚拟机未崩溃的情况"""
        mock_exec.return_value = {"code": 0, "stdout": "running", "stderr": ""}
        mock_exists.return_value = False
        
        result = get_vm_crash_status("test-vm")
        result_dict = json.loads(result)
        
        self.assertEqual(result_dict["vm_name"], "test-vm")
        self.assertFalse(result_dict["crashed"])
        self.assertTrue(result_dict["success"])

    @patch('gather.get_vm_crash_status.execute_cmd')
    @patch('gather.get_vm_crash_status.os.path.exists')
    @patch('builtins.open')
    def test_get_vm_crash_status_crashed(self, mock_open, mock_exists, mock_exec):
        """测试虚拟机崩溃的情况"""
        mock_exec.return_value = {"code": 0, "stdout": "crashed", "stderr": ""}
        mock_exists.return_value = True
        
        mock_file = MagicMock()
        mock_file.__enter__ = MagicMock(return_value=mock_file)
        mock_file.__exit__ = MagicMock(return_value=False)
        mock_file.readlines.return_value = ["kernel panic: test error"]
        mock_open.return_value = mock_file
        
        result = get_vm_crash_status("test-vm")
        result_dict = json.loads(result)
        
        self.assertTrue(result_dict["crashed"])
        self.assertIn("崩溃", result_dict["crash_reason"])

    @patch('gather.get_vm_crash_status.execute_cmd')
    def test_get_vm_crash_status_command_failed(self, mock_exec):
        """测试获取虚拟机状态失败"""
        mock_exec.return_value = {"code": 1, "stdout": "", "stderr": "error"}
        
        result = get_vm_crash_status("test-vm")
        result_dict = json.loads(result)
        
        self.assertFalse(result_dict["success"])
        self.assertIn("获取虚机状态失败", result_dict["error"])


if __name__ == '__main__':
    unittest.main(verbosity=2)
