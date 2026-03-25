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
import unittest
from unittest.mock import patch
import json

from gather import get_vm_network_rx_tx_stats

class TestVMNetworkRxTxStats(unittest.TestCase):

    # =========================
    # execute_cmd
    # =========================
    @patch("gather.get_vm_network_rx_tx_stats.subprocess.run")
    def test_execute_cmd_success(self, mock_run):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "ok\n"
        mock_run.return_value.stderr = ""
        result = get_vm_network_rx_tx_stats.execute_cmd(["ls"])
        self.assertEqual(result["code"], 0)
        self.assertEqual(result["stdout"], "ok")

    @patch("gather.get_vm_network_rx_tx_stats.subprocess.run")
    def test_execute_cmd_timeout(self, mock_run):
        from subprocess import TimeoutExpired
        mock_run.side_effect = TimeoutExpired(cmd="cmd", timeout=30)
        result = get_vm_network_rx_tx_stats.execute_cmd(["cmd"])
        self.assertNotEqual(result["code"], 0)
        self.assertIn("超时", result["stderr"])

    # =========================
    # get_vm_nic_list
    # =========================
    @patch("gather.get_vm_network_rx_tx_stats.execute_cmd")
    def test_get_vm_nic_list_success(self, mock_cmd):
        mock_cmd.return_value = {
            "code": 0,
            "stdout": """Interface  Type       Source     Model       MAC
------------------------------------------------------------
vnet0      bridge     br0        virtio      52:54:00:xx:xx:xx
"""
        }
        result = get_vm_network_rx_tx_stats.get_vm_nic_list("vm1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["interface"], "vnet0")

    @patch("gather.get_vm_network_rx_tx_stats.execute_cmd")
    def test_get_vm_nic_list_fail(self, mock_cmd):
        mock_cmd.return_value = {"code": 1, "stdout": "", "stderr": "error"}
        result = get_vm_network_rx_tx_stats.get_vm_nic_list("vm1")
        self.assertEqual(result, [])

    # =========================
    # get_vm_list
    # =========================
    @patch("gather.get_vm_network_rx_tx_stats.execute_cmd")
    def test_get_vm_list_success(self, mock_cmd):
        mock_cmd.return_value = {
            "code": 0,
            "stdout": "vm1\nvm2\n"
        }
        result = get_vm_network_rx_tx_stats.get_vm_list()
        self.assertEqual(result, ["vm1", "vm2"])

    @patch("gather.get_vm_network_rx_tx_stats.execute_cmd")
    def test_get_vm_list_fail(self, mock_cmd):
        mock_cmd.return_value = {"code": 1, "stdout": "", "stderr": ""}
        result = get_vm_network_rx_tx_stats.get_vm_list()
        self.assertEqual(result, [])

    # =========================
    # get_vm_network_rx_tx_stats
    # =========================
    @patch("gather.get_vm_network_rx_tx_stats.execute_cmd")
    @patch("gather.get_vm_network_rx_tx_stats.get_vm_nic_list")
    def test_get_vm_network_stats_success(self, mock_nics, mock_cmd):
        mock_nics.return_value = [
            {"interface": "vnet0"}
        ]
        mock_cmd.return_value = {
            "code": 0,
            "stdout": """vnet0 rx_bytes 100
vnet0 rx_packets 10
vnet0 tx_bytes 200
vnet0 tx_packets 20
"""
        }
        result_json = get_vm_network_rx_tx_stats.get_vm_network_rx_tx_stats("vm1")
        result = json.loads(result_json)
        self.assertTrue(result["success"])
        self.assertEqual(len(result["nics"]), 1)
        self.assertEqual(result["nics"][0]["rx_bytes"], 100)
        self.assertEqual(result["nics"][0]["tx_bytes"], 200)

    @patch("gather.get_vm_network_rx_tx_stats.get_vm_nic_list")
    def test_get_vm_network_stats_no_nics(self, mock_nics):
        mock_nics.return_value = []
        result_json = get_vm_network_rx_tx_stats.get_vm_network_rx_tx_stats("vm1")
        result = json.loads(result_json)
        self.assertFalse(result["success"])
        self.assertIn("未获取到虚机网卡列表", result["error"])

if __name__ == "__main__":
    unittest.main()
