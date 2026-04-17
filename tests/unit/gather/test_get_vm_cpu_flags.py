#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
from unittest.mock import patch, MagicMock
import subprocess
import json
import base64

from gather import get_vm_cpu_flags

class TestGetVmCpuFlags(unittest.TestCase):

    # =========================
    # run_virsh_cmd
    # =========================
    @patch("gather.get_vm_cpu_flags.subprocess.run")
    def test_run_virsh_cmd_success(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="ok",
            stderr=""
        )
        result = get_vm_cpu_flags.run_virsh_cmd("cmd")
        self.assertEqual(result, "ok")

    @patch("gather.get_vm_cpu_flags.subprocess.run")
    def test_run_virsh_cmd_fail(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="error"
        )
        result = get_vm_cpu_flags.run_virsh_cmd("cmd")
        self.assertIsNone(result)

    @patch("gather.get_vm_cpu_flags.subprocess.run")
    def test_run_virsh_cmd_timeout(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd="cmd",
            timeout=30
        )
        result = get_vm_cpu_flags.run_virsh_cmd("cmd")
        self.assertIsNone(result)

    @patch("gather.get_vm_cpu_flags.subprocess.run")
    def test_run_virsh_cmd_exception(self, mock_run):
        mock_run.side_effect = Exception("boom")
        result = get_vm_cpu_flags.run_virsh_cmd("cmd")
        self.assertIsNone(result)

    # =========================
    # get_domain_uuid
    # =========================
    @patch("gather.get_vm_cpu_flags.run_virsh_cmd")
    def test_get_domain_uuid_success(self, mock_run):
        mock_run.return_value = "uuid-123"
        result = get_vm_cpu_flags.get_domain_uuid("vm1")
        self.assertEqual(result, "uuid-123")

    @patch("gather.get_vm_cpu_flags.run_virsh_cmd")
    def test_get_domain_uuid_fail(self, mock_run):
        mock_run.return_value = None
        result = get_vm_cpu_flags.get_domain_uuid("vm1")
        self.assertIsNone(result)

    # =========================
    # get_vm_cpu_flags_via_qga
    # =========================
    @patch("gather.get_vm_cpu_flags.time.sleep")
    @patch("gather.get_vm_cpu_flags.run_virsh_cmd")
    def test_get_vm_cpu_flags_via_qga_success(
        self,
        mock_run,
        mock_sleep
    ):
        flags_line = "flags : fpu vme sse sse2"
        encoded = base64.b64encode(
            flags_line.encode()
        ).decode()
        first_resp = json.dumps({
            "return": {
                "pid": 100
            }
        })
        second_resp = json.dumps({
            "return": {
                "exited": True,
                "out-data": encoded
            }
        })
        mock_run.side_effect = [
            first_resp,
            second_resp
        ]

        result = (
            get_vm_cpu_flags
            .get_vm_cpu_flags_via_qga("vm1")
        )
        self.assertEqual(
            result,
            ["fpu", "vme", "sse", "sse2"]
        )

    @patch("gather.get_vm_cpu_flags.run_virsh_cmd")
    def test_get_vm_cpu_flags_via_qga_no_pid(
        self,
        mock_run
    ):
        mock_run.return_value = json.dumps({
            "return": {}
        })
        result = (
            get_vm_cpu_flags
            .get_vm_cpu_flags_via_qga("vm1")
        )
        self.assertIsNone(result)

    @patch("gather.get_vm_cpu_flags.time.sleep")
    @patch("gather.get_vm_cpu_flags.run_virsh_cmd")
    def test_get_vm_cpu_flags_via_qga_not_exited(
        self,
        mock_run,
        mock_sleep
    ):
        first_resp = json.dumps({
            "return": {
                "pid": 10
            }
        })
        second_resp = json.dumps({
            "return": {
                "exited": False
            }
        })
        mock_run.side_effect = [
            first_resp,
            second_resp
        ]
        result = (
            get_vm_cpu_flags
            .get_vm_cpu_flags_via_qga("vm1")
        )
        self.assertIsNone(result)

    @patch("gather.get_vm_cpu_flags.time.sleep")
    @patch("gather.get_vm_cpu_flags.run_virsh_cmd")
    def test_get_vm_cpu_flags_via_qga_no_output(
        self,
        mock_run,
        mock_sleep
    ):
        first_resp = json.dumps({
            "return": {
                "pid": 10
            }
        })
        second_resp = json.dumps({
            "return": {
                "exited": True,
                "out-data": ""
            }
        })
        mock_run.side_effect = [
            first_resp,
            second_resp
        ]
        result = (
            get_vm_cpu_flags
            .get_vm_cpu_flags_via_qga("vm1")
        )
        self.assertIsNone(result)

    @patch("gather.get_vm_cpu_flags.run_virsh_cmd")
    def test_get_vm_cpu_flags_via_qga_parse_error(
        self,
        mock_run
    ):
        mock_run.return_value = "invalid json"
        result = (
            get_vm_cpu_flags
            .get_vm_cpu_flags_via_qga("vm1")
        )
        self.assertIsNone(result)

    # =========================
    # get_vm_cpu_flags
    # =========================
    @patch("gather.get_vm_cpu_flags.time.time")
    @patch("gather.get_vm_cpu_flags.get_vm_cpu_flags_via_qga")
    @patch("gather.get_vm_cpu_flags.get_domain_uuid")
    def test_get_vm_cpu_flags_success(
        self,
        mock_uuid,
        mock_flags,
        mock_time
    ):
        mock_uuid.return_value = "uuid-1"
        mock_flags.return_value = [
            "fpu",
            "sse"
        ]
        mock_time.return_value = 123456
        result = (
            get_vm_cpu_flags
            .get_vm_cpu_flags("vm1")
        )
        self.assertEqual(
            result["vm_name"],
            "vm1"
        )
        self.assertEqual(
            result["flags_count"],
            2
        )
        self.assertEqual(
            result["timestamp"],
            123456
        )

    @patch("gather.get_vm_cpu_flags.get_domain_uuid")
    def test_get_vm_cpu_flags_uuid_none(
        self,
        mock_uuid
    ):
        mock_uuid.return_value = None
        result = (
            get_vm_cpu_flags
            .get_vm_cpu_flags("vm1")
        )
        self.assertEqual(
            result,
            {}
        )

    @patch("gather.get_vm_cpu_flags.get_vm_cpu_flags_via_qga")
    @patch("gather.get_vm_cpu_flags.get_domain_uuid")
    def test_get_vm_cpu_flags_flags_none(
        self,
        mock_uuid,
        mock_flags
    ):
        mock_uuid.return_value = "uuid"
        mock_flags.return_value = None
        result = (
            get_vm_cpu_flags
            .get_vm_cpu_flags("vm1")
        )
        self.assertEqual(
            result,
            {}
        )

if __name__ == "__main__":
    unittest.main()
