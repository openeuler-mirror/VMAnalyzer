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

from gather import get_vm_bc_diskstats

class TestVMCollector(unittest.TestCase):

    def setUp(self):
        self.collector = get_vm_bc_diskstats.VMCollector(output_dir="/tmp/test")

    # -----------------------------
    # run_virsh_cmd
    # -----------------------------
    @patch("gather.get_vm_bc_diskstats.subprocess.run")
    def test_run_virsh_cmd_success(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "running\n"
        mock_run.return_value = mock_result
        result = self.collector.run_virsh_cmd("virsh domstate vm1")
        self.assertEqual(result, "running")

    @patch("gather.get_vm_bc_diskstats.subprocess.run")
    def test_run_virsh_cmd_failed(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd="virsh",
            stderr="error"
        )
        result = self.collector.run_virsh_cmd("virsh domstate vm1")
        self.assertIsNone(result)

    # -----------------------------
    # get_vm_state
    # -----------------------------
    @patch.object(get_vm_bc_diskstats.VMCollector, "run_virsh_cmd")
    def test_get_vm_state(self, mock_cmd):
        mock_cmd.return_value = "Running"
        state = self.collector.get_vm_state("vm1")
        self.assertEqual(state, "running")

    # -----------------------------
    # get_all_vm_names
    # -----------------------------
    @patch.object(get_vm_bc_diskstats.VMCollector, "run_virsh_cmd")
    def test_get_all_vm_names(self, mock_cmd):
        mock_cmd.return_value = "vm1\nvm2\n"
        result = self.collector.get_all_vm_names()
        self.assertEqual(result, ["vm1", "vm2"])

    # -----------------------------
    # call_qga_interface
    # -----------------------------
    @patch.object(get_vm_bc_diskstats.VMCollector, "run_virsh_cmd")
    def test_call_qga_interface_success(self, mock_cmd):
        mock_cmd.return_value = json.dumps({
            "return": {"disk": "data"}
        })
        result = self.collector.call_qga_interface("vm1", "bc-guest-get-diskstats")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"], {"disk": "data"})

    @patch.object(get_vm_bc_diskstats.VMCollector, "run_virsh_cmd")
    def test_call_qga_interface_parse_error(self, mock_cmd):
        mock_cmd.return_value = "invalid json"
        result = self.collector.call_qga_interface("vm1", "bc-guest-get-diskstats")
        self.assertEqual(result["status"], "parse_error")

    # -----------------------------
    # collect_single_vm_data
    # -----------------------------
    @patch.object(get_vm_bc_diskstats.VMCollector, "call_qga_interface")
    @patch.object(get_vm_bc_diskstats.VMCollector, "get_vm_state")
    def test_collect_single_vm_data(self, mock_state, mock_qga):
        mock_state.return_value = "running"
        mock_qga.return_value = {
            "status": "success",
            "data": {"disk": "data"},
            "error": ""
        }
        result = self.collector.collect_single_vm_data("vm1")
        self.assertEqual(result["name"], "vm1")
        self.assertEqual(result["state"], "running")

    # -----------------------------
    # collect_all_vms
    # -----------------------------
    @patch.object(get_vm_bc_diskstats.VMCollector, "collect_single_vm_data")
    @patch.object(get_vm_bc_diskstats.VMCollector, "get_all_vm_names")
    def test_collect_all_vms(self, mock_names, mock_collect):
        mock_names.return_value = ["vm1", "vm2"]
        mock_collect.return_value = {"name": "vm1"}

if __name__ == "__main__":
    unittest.main()
