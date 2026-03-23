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
from unittest.mock import patch, MagicMock, mock_open
import json

from gather import get_vm_tcp_stats

class TestVMQgaTCPCollector(unittest.TestCase):

    @patch("gather.get_vm_tcp_stats.subprocess.run")
    def test_run_virsh_cmd_success(self, mock_run):
        """测试 run_virsh_cmd 正常返回"""
        mock_run.return_value = MagicMock(stdout="output\n", stderr="", returncode=0)
        collector = get_vm_tcp_stats.VMQgaTCPCollector()
        result = collector.run_virsh_cmd("virsh list")
        self.assertEqual(result, "output")

    @patch("gather.get_vm_tcp_stats.subprocess.run")
    def test_run_virsh_cmd_error(self, mock_run):
        """测试 run_virsh_cmd 命令出错"""
        mock_run.side_effect = get_vm_tcp_stats.subprocess.CalledProcessError(
            1, "cmd", stderr="some error"
        )
        collector = get_vm_tcp_stats.VMQgaTCPCollector()
        result = collector.run_virsh_cmd("virsh fail")
        self.assertIsNone(result)

    @patch("gather.get_vm_tcp_stats.VMQgaTCPCollector.run_virsh_cmd")
    def test_get_all_vm_names(self, mock_run_cmd):
        mock_run_cmd.return_value = "vm1 vm2\n"
        collector = get_vm_tcp_stats.VMQgaTCPCollector()
        names = collector.get_all_vm_names()
        self.assertEqual(names, ["vm1", "vm2"])

    @patch("gather.get_vm_tcp_stats.VMQgaTCPCollector.run_virsh_cmd")
    def test_get_vm_state(self, mock_run_cmd):
        mock_run_cmd.return_value = "running"
        collector = get_vm_tcp_stats.VMQgaTCPCollector()
        state = collector.get_vm_state("vm1")
        self.assertEqual(state, "running")

    @patch("gather.get_vm_tcp_stats.VMQgaTCPCollector.get_vm_state")
    def test_is_vm_running(self, mock_get_vm_state):
        mock_get_vm_state.return_value = "running"
        collector = get_vm_tcp_stats.VMQgaTCPCollector()
        self.assertTrue(collector.is_vm_running("vm1"))
        mock_get_vm_state.return_value = "shut off"
        self.assertFalse(collector.is_vm_running("vm2"))

    @patch("gather.get_vm_tcp_stats.VMQgaTCPCollector.is_vm_running")
    @patch("gather.get_vm_tcp_stats.VMQgaTCPCollector.run_virsh_cmd")
    def test_call_qga_interface_success(self, mock_run_cmd, mock_is_running):
        mock_is_running.return_value = True
        mock_run_cmd.return_value = '{"return":{"retranssegs":10,"outsegs":100}}'
        collector = get_vm_tcp_stats.VMQgaTCPCollector()
        result = collector.call_qga_interface("vm1", "bc-guest-get-tcp-snmp")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["retranssegs"], 10)

    @patch("gather.get_vm_tcp_stats.VMQgaTCPCollector.is_vm_running")
    def test_call_qga_interface_vm_not_running(self, mock_is_running):
        mock_is_running.return_value = False
        collector = get_vm_tcp_stats.VMQgaTCPCollector()
        result = collector.call_qga_interface("vm1", "bc-guest-get-tcp-snmp")
        self.assertEqual(result["status"], "vm_not_running")

    def test_calculate_tcp_retrans_rate(self):
        collector = get_vm_tcp_stats.VMQgaTCPCollector()
        rate = collector.calculate_tcp_retrans_rate({"retranssegs": 5, "outsegs": 100})
        self.assertAlmostEqual(rate, 5.0)
        # outsegs 为 0
        rate = collector.calculate_tcp_retrans_rate({"retranssegs": 1, "outsegs": 0})
        self.assertEqual(rate, 0.0)

    @patch("gather.get_vm_tcp_stats.VMQgaTCPCollector.get_all_vm_names")
    @patch("gather.get_vm_tcp_stats.VMQgaTCPCollector.is_vm_running")
    @patch("gather.get_vm_tcp_stats.VMQgaTCPCollector.collect_single_vm_tcp_data")
    def test_collect_all_vms(self, mock_collect_single, mock_is_running, mock_get_names):
        mock_get_names.return_value = ["vm1", "vm2"]
        mock_is_running.side_effect = [True, False]
        mock_collect_single.side_effect = [{"name": "vm1"}, {"name": "vm2"}]
        collector = get_vm_tcp_stats.VMQgaTCPCollector()
        collector.collect_all_vms()
        self.assertEqual(collector.all_vms_data["vm_count"], 2)
        self.assertEqual(collector.all_vms_data["running_vm_count"], 1)
        self.assertIn("vm1", collector.all_vms_data["vms"])
        self.assertIn("vm2", collector.all_vms_data["vms"])

    @patch("gather.get_vm_tcp_stats.open", new_callable=mock_open)
    def test_save_to_json(self, mock_file):
        collector = get_vm_tcp_stats.VMQgaTCPCollector()
        collector.all_vms_data = {"vm_count": 1}
        collector.save_to_json("test.json")
