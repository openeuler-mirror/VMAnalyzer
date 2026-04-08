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

from gather import get_vm_disk_actual_size

class TestVMDiskActualSize(unittest.TestCase):

    # =========================
    # execute_cmd
    # =========================
    @patch("gather.get_vm_disk_actual_size.subprocess.run")
    def test_execute_cmd_success(self, mock_run):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "ok\n"
        mock_run.return_value.stderr = ""
        result = get_vm_disk_actual_size.execute_cmd(["ls"])
        self.assertEqual(result["code"], 0)
        self.assertEqual(result["stdout"], "ok")

    @patch("gather.get_vm_disk_actual_size.subprocess.run")
    def test_execute_cmd_timeout(self, mock_run):
        from subprocess import TimeoutExpired
        mock_run.side_effect = TimeoutExpired(cmd="cmd", timeout=30)
        result = get_vm_disk_actual_size.execute_cmd(["cmd"])
        self.assertIn("超时", result["stderr"])

    # =========================
    # get_vm_disk_list
    # =========================
    @patch("gather.get_vm_disk_actual_size.execute_cmd")
    def test_get_vm_disk_list_success(self, mock_cmd):
        mock_cmd.return_value = {
            "code": 0,
            "stdout": """Type       Device     Target     Source
------------------------------------------------
file       disk       vda        /path/disk.qcow2
"""
        }
        result = get_vm_disk_actual_size.get_vm_disk_list("vm1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["target"], "vda")

    @patch("gather.get_vm_disk_actual_size.execute_cmd")
    def test_get_vm_disk_list_fail(self, mock_cmd):
        mock_cmd.return_value = {
            "code": 1,
            "stdout": "",
            "stderr": "error"
        }
        result = get_vm_disk_actual_size.get_vm_disk_list("vm1")
        if isinstance(result, tuple):
            result = result[0]
        self.assertEqual(result, [])

    # =========================
    # get_vm_list
    # =========================
    @patch("gather.get_vm_disk_actual_size.execute_cmd")
    def test_get_vm_list(self, mock_cmd):
        mock_cmd.return_value = {
            "code": 0,
            "stdout": "vm1\nvm2\n"
        }
        result = get_vm_disk_actual_size.get_vm_list()
        self.assertEqual(result, ["vm1", "vm2"])

    # =========================
    # get_vm_disk_actual_size
    # =========================
    @patch("gather.get_vm_disk_actual_size.os.path.exists")
    @patch("gather.get_vm_disk_actual_size.execute_cmd")
    @patch("gather.get_vm_disk_actual_size.get_vm_disk_list")
    def test_get_disk_size_success(self, mock_disk_list, mock_cmd, mock_exists):
        mock_disk_list.return_value = [
            {"target": "vda", "source": "/disk.qcow2"}
        ]
        mock_exists.return_value = True
        mock_cmd.return_value = {
            "code": 0,
            "stdout": json.dumps({
                "actual-size": 100,
                "virtual-size": 200
            })
        }
        result_json = get_vm_disk_actual_size.get_vm_disk_actual_size("vm1")
        result = json.loads(result_json)
        self.assertTrue(result["success"])
        self.assertEqual(result["disks"][0]["actual_size"], 100)
        self.assertEqual(result["disks"][0]["virtual_size"], 200)
        self.assertEqual(result["disks"][0]["usage_rate"], 0.5)

    @patch("gather.get_vm_disk_actual_size.get_vm_disk_list")
    def test_get_disk_size_no_disks(self, mock_disk_list):
        mock_disk_list.return_value = []
        result_json = get_vm_disk_actual_size.get_vm_disk_actual_size("vm1")
        result = json.loads(result_json)
        self.assertFalse(result["success"])
        self.assertIn("未获取到虚机磁盘列表", result["error"])

    @patch("gather.get_vm_disk_actual_size.os.path.exists")
    @patch("gather.get_vm_disk_actual_size.get_vm_disk_list")
    def test_get_disk_path_not_exist(self, mock_disk_list, mock_exists):
        mock_disk_list.return_value = [
            {"target": "vda", "source": "/not_exist.qcow2"}
        ]
        mock_exists.return_value = False
        result_json = get_vm_disk_actual_size.get_vm_disk_actual_size("vm1")
        result = json.loads(result_json)
        self.assertEqual(result["disks"][0]["error"], "磁盘source路径为空")

    @patch("gather.get_vm_disk_actual_size.os.path.exists")
    @patch("gather.get_vm_disk_actual_size.execute_cmd")
    @patch("gather.get_vm_disk_actual_size.get_vm_disk_list")
    def test_get_disk_json_parse_error(self, mock_disk_list, mock_cmd, mock_exists):
        mock_disk_list.return_value = [
            {"target": "vda", "source": "/disk.qcow2"}
        ]
        mock_exists.return_value = True
        mock_cmd.return_value = {
            "code": 0,
            "stdout": "invalid json"
        }
        result_json = get_vm_disk_actual_size.get_vm_disk_actual_size("vm1")
        result = json.loads(result_json)
        self.assertIn("JSON解析失败", result["disks"][0]["error"])

if __name__ == "__main__":
    unittest.main()
