#!/usr/bin/env python3
# _*_coding: utf-8 _*_

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
import unittest
import json
from unittest.mock import patch, MagicMock

from gather.get_vm_host_mem_usage import get_vm_pid, get_vm_host_mem_usage


class TestGetVmPid(unittest.TestCase):

    @patch('gather.get_vm_host_mem_usage.execute_cmd')
    def test_finds_pid(self, mock_exec):
        mock_exec.return_value = {
            'code': 0,
            'stdout': 'root 1234 0.5 5.0 /usr/bin/qemu-kvm -name guest=test-vm',
            'stderr': ''
        }
        pid = get_vm_pid('test-vm')
        self.assertEqual(pid, '1234')

    @patch('gather.get_vm_host_mem_usage.execute_cmd')
    def test_returns_empty_when_not_found(self, mock_exec):
        mock_exec.return_value = {
            'code': 0,
            'stdout': 'root 999 0.0 0.0 bash',
            'stderr': ''
        }
        pid = get_vm_pid('nonexistent-vm')
        self.assertEqual(pid, '')

    @patch('gather.get_vm_host_mem_usage.execute_cmd')
    def test_returns_empty_on_cmd_error(self, mock_exec):
        mock_exec.return_value = {'code': 1, 'stdout': '', 'stderr': 'error'}
        pid = get_vm_pid('test-vm')
        self.assertEqual(pid, '')


class TestGetVmHostMemUsage(unittest.TestCase):

    def test_empty_pid_returns_error(self):
        with patch('gather.get_vm_host_mem_usage.get_vm_pid', return_value=''):
            result_json = get_vm_host_mem_usage('test-vm')
            result = json.loads(result_json)
            self.assertFalse(result['success'])
            self.assertIn('未找到', result['error'])

    def test_non_digit_pid_returns_error(self):
        with patch('gather.get_vm_host_mem_usage.get_vm_pid', return_value='abc'):
            result_json = get_vm_host_mem_usage('test-vm')
            result = json.loads(result_json)
            self.assertFalse(result['success'])

    @patch('gather.get_vm_host_mem_usage.psutil.virtual_memory')
    @patch('gather.get_vm_host_mem_usage.psutil.Process')
    @patch('gather.get_vm_host_mem_usage.get_vm_pid')
    def test_valid_pid_returns_memory_info(self, mock_pid, mock_process, mock_vmem):
        mock_pid.return_value = '1234'
        mock_mem_info = MagicMock()
        mock_mem_info.rss = 2 * 1024 * 1024 * 1024   # 2 GB
        mock_mem_info.vms = 4 * 1024 * 1024 * 1024   # 4 GB
        mock_process.return_value.memory_info.return_value = mock_mem_info
        mock_vmem.return_value.total = 16 * 1024 * 1024 * 1024  # 16 GB
        result_json = get_vm_host_mem_usage('test-vm')
        result = json.loads(result_json)
        self.assertTrue(result['success'])
        self.assertAlmostEqual(result['rss_mb'], 2048.0, places=1)
        self.assertAlmostEqual(result['vsz_mb'], 4096.0, places=1)
        self.assertAlmostEqual(result['mem_percent'], 12.5, places=1)

    @patch('gather.get_vm_host_mem_usage.psutil.Process')
    @patch('gather.get_vm_host_mem_usage.get_vm_pid')
    def test_no_such_process_returns_error(self, mock_pid, mock_process):
        import psutil
        mock_pid.return_value = '9999'
        mock_process.return_value.memory_info.side_effect = psutil.NoSuchProcess(9999)
        result_json = get_vm_host_mem_usage('test-vm')
        result = json.loads(result_json)
        self.assertFalse(result['success'])
        self.assertIn('已退出', result['error'])


if __name__ == '__main__':
    unittest.main()
