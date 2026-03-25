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
import subprocess
import json

from gather import get_vm_network_interfaces_info

class TestVMCollector(unittest.TestCase):

    def setUp(self):
        self.collector = get_vm_network_interfaces_info.VMCollector(
            output_dir="/tmp/test_network"
        )

    # =========================
    # run_virsh_cmd
    # =========================
    @patch("gather.get_vm_network_interfaces_info.subprocess.run")
    def test_run_virsh_cmd_success(self, mock_run):
        mock_res = MagicMock()
        mock_res.stdout = "output\n"
        mock_run.return_value = mock_res
        result = self.collector.run_virsh_cmd("virsh list")
        self.assertEqual(result, "output")

    @patch("gather.get_vm_network_interfaces_info.subprocess.run")
    def test_run_virsh_cmd_fail(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd="cmd", stderr="error"
        )
        result = self.collector.run_virsh_cmd("cmd")
        self.assertIsNone(result)

    @patch("gather.get_vm_network_interfaces_info.subprocess.run")
    def test_run_virsh_cmd_timeout(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="cmd", timeout=30)
        result = self.collector.run_virsh_cmd("cmd")
        self.assertIsNone(result)

    # =========================
    # get_all_vm_names
    # =========================
    @patch.object(get_vm_network_interfaces_info.VMCollector, "run_virsh_cmd")
    def test_get_all_vm_names(self, mock_cmd):
        mock_cmd.return_value = "vm1\nvm2\n"
        result = self.collector.get_all_vm_names()
        self.assertEqual(result, ["vm1", "vm2"])

    @patch.object(get_vm_network_interfaces_info.VMCollector, "run_virsh_cmd")
    def test_get_all_vm_names_empty(self, mock_cmd):
        mock_cmd.return_value = None
        result = self.collector.get_all_vm_names()
        self.assertEqual(result, [])

    # =========================
    # call_qga_interface
    # =========================

    @patch.object(get_vm_network_interfaces_info.VMCollector, "run_virsh_cmd")
    def test_call_qga_interface_success(self, mock_cmd):
        mock_cmd.return_value = json.dumps({
            "return": {"eth0": "info"}
        })

    @patch.object(get_vm_network_interfaces_info.VMCollector, "run_virsh_cmd")
    def test_call_qga_interface_fail(self, mock_cmd):
        mock_cmd.return_value = None
        result = self.collector.call_qga_interface("vm1", "iface")
        self.assertEqual(result["status"], "failed")

    @patch.object(get_vm_network_interfaces_info.VMCollector, "run_virsh_cmd")
    def test_call_qga_interface_parse_error(self, mock_cmd):
        mock_cmd.return_value = "invalid json"

if __name__ == "__main__":
    unittest.main()
