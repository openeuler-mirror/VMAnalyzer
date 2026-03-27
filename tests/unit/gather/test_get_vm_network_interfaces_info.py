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
        result = self.collector.call_qga_interface("vm1", "iface")
        self.assertEqual(result["status"], "parse_error")

    @patch.object(get_vm_network_interfaces_info.VMCollector, "run_virsh_cmd")
    def test_call_qga_interface_no_return_field(self, mock_cmd):
        mock_cmd.return_value = json.dumps({
            "error": {"message": "bad"}
        })
        result = self.collector.call_qga_interface("vm1", "iface")
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["error"], "bad")

    # =========================
    # collect_single_vm_cpustinfo_data
    # =========================
    @patch.object(get_vm_network_interfaces_info.VMCollector, "call_qga_interface")
    def test_collect_single_vm(self, mock_call):
        mock_call.return_value = {
            "status": "success",
            "data": {"eth0": "info"},
            "error": ""
        }
        result = self.collector.collect_single_vm_cpustinfo_data("vm1")
        self.assertEqual(result["name"], "vm1")
        self.assertIn("get_network_info", result)

    # =========================
    # collect_all_vms
    # =========================
    @patch.object(get_vm_network_interfaces_info.VMCollector, "collect_single_vm_cpustinfo_data")
    @patch.object(get_vm_network_interfaces_info.VMCollector, "get_all_vm_names")
    def test_collect_all_vms(self, mock_vms, mock_single):
        mock_vms.return_value = ["vm1"]
        mock_single.return_value = {"name": "vm1"}
        self.collector.collect_all_vms()
        self.assertEqual(self.collector.all_vms_data["vm_count"], 1)
        self.assertEqual(self.collector.all_vms_data["running_vm_count"], 1)
        self.assertIn("vm1", self.collector.all_vms_data["vms"])

    @patch.object(get_vm_network_interfaces_info.VMCollector, "get_all_vm_names")
    def test_collect_all_vms_empty(self, mock_vms):
        mock_vms.return_value = []
        self.collector.collect_all_vms()

    # =========================
    # save_data
    # =========================
    @patch("gather.get_vm_network_interfaces_info.open", new_callable=mock_open)
    @patch("gather.get_vm_network_interfaces_info.json.dump")
    def test_save_data(self, mock_dump, mock_file):
        self.collector.save_data()
        mock_dump.assert_called()

if __name__ == "__main__":
    unittest.main()
