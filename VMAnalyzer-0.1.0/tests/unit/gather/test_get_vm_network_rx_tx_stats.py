#!/usr/bin/env python3
# _*_coding: utf-8 _*_

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
import unittest
import json
from unittest.mock import patch, MagicMock

from gather.get_vm_network_rx_tx_stats import (
    execute_cmd, get_vm_nic_list, get_vm_list, get_vm_network_rx_tx_stats
)


class TestExecuteCmd(unittest.TestCase):

    @patch('gather.get_vm_network_rx_tx_stats.subprocess.run')
    def test_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout='output\n', stderr='')
        result = execute_cmd(['echo', 'output'])
        self.assertEqual(result['code'], 0)
        self.assertEqual(result['stdout'], 'output')

    @patch('gather.get_vm_network_rx_tx_stats.subprocess.run')
    def test_timeout(self, mock_run):
        import subprocess
        mock_run.side_effect = subprocess.TimeoutExpired(cmd='cmd', timeout=30)
        result = execute_cmd(['sleep', '100'])
        self.assertNotEqual(result['code'], 0)
        self.assertIn('超时', result['stderr'])

    @patch('gather.get_vm_network_rx_tx_stats.subprocess.run')
    def test_generic_exception(self, mock_run):
        mock_run.side_effect = OSError('no such file')
        result = execute_cmd(['nonexistent'])
        self.assertEqual(result['code'], -1)
        self.assertIn('异常', result['stderr'])


class TestGetVmList(unittest.TestCase):

    @patch('gather.get_vm_network_rx_tx_stats.execute_cmd')
    def test_returns_vm_names(self, mock_exec):
        mock_exec.return_value = {'code': 0, 'stdout': 'vm1\nvm2\nvm3', 'stderr': ''}
        result = get_vm_list()
        self.assertEqual(result, ['vm1', 'vm2', 'vm3'])

    @patch('gather.get_vm_network_rx_tx_stats.execute_cmd')
    def test_returns_empty_on_error(self, mock_exec):
        mock_exec.return_value = {'code': 1, 'stdout': '', 'stderr': 'error'}
        result = get_vm_list()
        self.assertEqual(result, [])


class TestGetVmNetworkRxTxStats(unittest.TestCase):

    def test_empty_vm_name_returns_error(self):
        result_json = get_vm_network_rx_tx_stats('   ')
        result = json.loads(result_json)
        self.assertFalse(result['success'])
        self.assertIn('不能为空', result['error'])

    @patch('gather.get_vm_network_rx_tx_stats.get_vm_nic_list')
    def test_no_nics_returns_error(self, mock_nic_list):
        mock_nic_list.return_value = []
        result_json = get_vm_network_rx_tx_stats('test-vm')
        result = json.loads(result_json)
        self.assertFalse(result['success'])
        self.assertIn('未获取到', result['error'])

    @patch('gather.get_vm_network_rx_tx_stats.execute_cmd')
    @patch('gather.get_vm_network_rx_tx_stats.get_vm_nic_list')
    def test_parses_nic_stats(self, mock_nic_list, mock_exec):
        mock_nic_list.return_value = [
            {'interface': 'vnet0', 'type': 'bridge', 'source': 'br0',
             'model': 'virtio', 'mac': 'fa:16:3e:00:00:01'}
        ]
        ifstat_output = (
            'vnet0 rx_bytes 12345\n'
            'vnet0 rx_packets 100\n'
            'vnet0 rx_errors 0\n'
            'vnet0 rx_dropped 0\n'
            'vnet0 tx_bytes 6789\n'
            'vnet0 tx_packets 50\n'
            'vnet0 tx_errors 0\n'
            'vnet0 tx_dropped 0\n'
        )
        mock_exec.return_value = {'code': 0, 'stdout': ifstat_output, 'stderr': ''}
        result_json = get_vm_network_rx_tx_stats('test-vm')
        result = json.loads(result_json)
        self.assertTrue(result['success'])
        self.assertEqual(len(result['nics']), 1)
        nic = result['nics'][0]
        self.assertEqual(nic['rx_bytes'], 12345)
        self.assertEqual(nic['tx_bytes'], 6789)


if __name__ == '__main__':
    unittest.main()
