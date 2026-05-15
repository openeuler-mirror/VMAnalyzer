#!/usr/bin/env python3
# _*_coding: utf-8 _*_

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
import unittest
import json
from unittest.mock import patch, MagicMock

try:
    import libvirt
    import libvirt_qemu
    HAS_LIBVIRT = True
except ImportError:
    HAS_LIBVIRT = False

from agent.get_premium_memory import QgaMemoryStatus


@unittest.skipUnless(HAS_LIBVIRT, 'libvirt not available')
class TestQgaMemoryStatus(unittest.TestCase):

    def _make_instance(self):
        with patch('agent.get_premium_memory.libvirt.open') as mock_open:
            mock_conn = MagicMock()
            mock_open.return_value = mock_conn
            instance = QgaMemoryStatus()
        return instance, mock_conn

    def test_memory_info_calculation(self):
        """测试内存信息计算正确性"""
        instance, mock_conn = self._make_instance()

        mock_dom = MagicMock()
        mock_dom.state.return_value = (libvirt.VIR_DOMAIN_RUNNING, 0)
        mock_conn.lookupByName.return_value = mock_dom

        qga_response = json.dumps({
            'return': {'total': 8192, 'available': 4096, 'free': 2048}
        })
        with patch('agent.get_premium_memory.libvirt_qemu.qemuAgentCommand',
                   return_value=qga_response):
            result = instance.execute_qga_memory_cmd('test-vm')

        self.assertEqual(result['status'], 'success')
        mem = result['memory_info']
        self.assertAlmostEqual(mem['total_mb'], 8192.0, places=1)
        self.assertAlmostEqual(mem['used_mb'], 4096.0, places=1)
        self.assertAlmostEqual(mem['free_mb'], 2048.0, places=1)
        self.assertAlmostEqual(mem['available_mb'], 4096.0, places=1)
        self.assertAlmostEqual(mem['usage_rate'], 50.0, places=1)

    def test_zero_total_gives_zero_usage_rate(self):
        """测试total为0时usage_rate为0.0，避免除零错误"""
        instance, mock_conn = self._make_instance()

        mock_dom = MagicMock()
        mock_dom.state.return_value = (libvirt.VIR_DOMAIN_RUNNING, 0)
        mock_conn.lookupByName.return_value = mock_dom

        qga_response = json.dumps({
            'return': {'total': 0, 'available': 0, 'free': 0}
        })
        with patch('agent.get_premium_memory.libvirt_qemu.qemuAgentCommand',
                   return_value=qga_response):
            result = instance.execute_qga_memory_cmd('test-vm')

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['memory_info']['usage_rate'], 0.0)

    def test_vm_not_running_returns_failed(self):
        """测试VM非运行状态时返回failed"""
        instance, mock_conn = self._make_instance()

        mock_dom = MagicMock()
        mock_dom.state.return_value = (libvirt.VIR_DOMAIN_SHUTOFF, 0)
        mock_conn.lookupByName.return_value = mock_dom

        result = instance.execute_qga_memory_cmd('test-vm')
        self.assertEqual(result['status'], 'failed')
        self.assertIn('非运行状态', result['error_msg'])

    def test_batch_execute_returns_list(self):
        """测试batch_execute返回多个结果"""
        instance, mock_conn = self._make_instance()

        mock_dom = MagicMock()
        mock_dom.state.return_value = (libvirt.VIR_DOMAIN_SHUTOFF, 0)
        mock_conn.lookupByName.return_value = mock_dom

        results = instance.batch_execute(['vm1', 'vm2'])
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['vm_name'], 'vm1')
        self.assertEqual(results[1]['vm_name'], 'vm2')

    def test_close_closes_connection(self):
        """测试close方法关闭libvirt连接"""
        instance, mock_conn = self._make_instance()
        instance.close()
        mock_conn.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
