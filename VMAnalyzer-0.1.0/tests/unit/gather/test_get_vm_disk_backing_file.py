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

from gather import get_vm_disk_backing_file

class TestVMDiskBackingFile(unittest.TestCase):

    # =========================
    # execute_cmd
    # =========================
    @patch("gather.get_vm_disk_backing_file.subprocess.run")
    def test_execute_cmd_success(self, mock_run):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "ok\n"
        mock_run.return_value.stderr = ""
        result = get_vm_disk_backing_file.execute_cmd(["ls"])
        self.assertEqual(result["code"], 0)
        self.assertEqual(result["stdout"], "ok")

    @patch("gather.get_vm_disk_backing_file.subprocess.run")
    def test_execute_cmd_timeout(self, mock_run):
        from subprocess import TimeoutExpired
        mock_run.side_effect = TimeoutExpired(cmd="cmd", timeout=30)
        result = get_vm_disk_backing_file.execute_cmd(["cmd"])
        self.assertIn("超时", result["stderr"])

    # =========================
    # get_vm_disk_list
    # =========================
    @patch("gather.get_vm_disk_backing_file.execute_cmd")
    def test_get_vm_disk_list_success(self, mock_cmd):
        mock_cmd.return_value = {
            "code": 0,
            "stdout": """Type       Device     Target     Source
------------------------------------------------
file       disk       vda        /path/disk.qcow2
"""
        }
        result = get_vm_disk_backing_file.get_vm_disk_list("vm1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["target"], "vda")

    @patch("gather.get_vm_disk_backing_file.execute_cmd")
    def test_get_vm_disk_list_fail(self, mock_cmd):
        mock_cmd.return_value = {
            "code": 1,
            "stdout": "",
            "stderr": "error"
        }
        result = get_vm_disk_backing_file.get_vm_disk_list("vm1")
        self.assertEqual(result, [])

    # =========================
    # get_vm_list
    # =========================
    @patch("gather.get_vm_disk_backing_file.execute_cmd")
    def test_get_vm_list(self, mock_cmd):
        mock_cmd.return_value = {
            "code": 0,
            "stdout": "vm1\nvm2\n"
        }
        result = get_vm_disk_backing_file.get_vm_list()
        self.assertEqual(result, ["vm1", "vm2"])
