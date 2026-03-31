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

from gather import get_vm_snapshot_info

class TestVMSnapshotInfo(unittest.TestCase):

    # =========================
    # execute_cmd
    # =========================
    @patch("gather.get_vm_snapshot_info.subprocess.run")
    def test_execute_cmd_success(self, mock_run):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "ok\n"
        mock_run.return_value.stderr = ""
        result = get_vm_snapshot_info.execute_cmd(["ls"])
        self.assertEqual(result["code"], 0)
        self.assertEqual(result["stdout"], "ok")

    @patch("gather.get_vm_snapshot_info.subprocess.run")
    def test_execute_cmd_timeout(self, mock_run):
        from subprocess import TimeoutExpired
        mock_run.side_effect = TimeoutExpired(
            cmd="cmd",
            timeout=30
        )
        result = get_vm_snapshot_info.execute_cmd(["cmd"])
        self.assertIn("超时", result["stderr"])

    # =========================
    # get_vm_list
    # =========================
    @patch("gather.get_vm_snapshot_info.execute_cmd")
    def test_get_vm_list_success(self, mock_cmd):
        mock_cmd.return_value = {
            "code": 0,
            "stdout": "vm1\nvm2\n"
        }
        result = get_vm_snapshot_info.get_vm_list()
        self.assertEqual(result, ["vm1", "vm2"])

    @patch("gather.get_vm_snapshot_info.execute_cmd")
    def test_get_vm_list_fail(self, mock_cmd):
        mock_cmd.return_value = {
            "code": 1,
            "stdout": "",
            "stderr": "error"
        }
        result = get_vm_snapshot_info.get_vm_list()
        self.assertEqual(result, [])

    # =========================
    # get_vm_snapshot_info
    # =========================
    @patch("gather.get_vm_snapshot_info.execute_cmd")
    def test_snapshot_info_success(self, mock_cmd):
        """完整成功路径"""
        mock_cmd.side_effect = [
            # snapshot-list
            {
                "code": 0,
                "stdout": """Name                 Creation Time             State
------------------------------------------------------------
snap1                2024-01-01 10:00:00      shutoff
"""
            },
            # snapshot-info
            {
                "code": 0,
                "stdout": """Name: snap1
State: shutoff
Current: yes
"""
            },
            # snapshot-dumpxml
            {
                "code": 0,
                "stdout": "<source file='/disk/snap1.qcow2'/>"
            },
            # qemu-img info
            {
                "code": 0,
                "stdout": json.dumps({
                    "virtual-size": 104857600
                })
            }
        ]
        result_json = get_vm_snapshot_info.get_vm_snapshot_info("vm1")
        result = json.loads(result_json)
        self.assertTrue(result["success"])
        self.assertEqual(len(result["snapshots"]), 1)
        snap = result["snapshots"][0]
        self.assertEqual(snap["name"], "snap1")
        self.assertEqual(snap["state"], "shutoff")
        self.assertTrue(snap["is_current"])
        self.assertEqual(snap["disk_size_mb"], 100.0)

    @patch("gather.get_vm_snapshot_info.execute_cmd")
    def test_snapshot_list_fail(self, mock_cmd):
        """snapshot-list 失败"""
        mock_cmd.return_value = {
            "code": 1,
            "stderr": "snapshot error",
            "stdout": ""
        }
        result_json = get_vm_snapshot_info.get_vm_snapshot_info("vm1")
        result = json.loads(result_json)
        self.assertFalse(result["success"])
        self.assertIn("snapshot error", result["error"])

    @patch("gather.get_vm_snapshot_info.execute_cmd")
    def test_snapshot_info_fail(self, mock_cmd):
        """snapshot-info 失败（应该跳过）"""
        mock_cmd.side_effect = [
            # snapshot-list
            {
                "code": 0,
                "stdout": """Name
----------------
snap1
"""
            },
            # snapshot-info fail
            {
                "code": 1,
                "stderr": "error"
            }
        ]
        result_json = get_vm_snapshot_info.get_vm_snapshot_info("vm1")
        result = json.loads(result_json)
        self.assertTrue(result["success"])
        self.assertEqual(len(result["snapshots"]), 0)

    @patch("gather.get_vm_snapshot_info.execute_cmd")
    def test_qemu_img_json_error(self, mock_cmd):
        """qemu-img JSON 解析失败"""
        mock_cmd.side_effect = [
            # snapshot-list
            {
                "code": 0,
                "stdout": """Name
----------------
snap1
"""
            },
            # snapshot-info
            {
                "code": 0,
                "stdout": """State: running
Current: no
"""
            },
            # snapshot-dumpxml
            {
                "code": 0,
                "stdout": "<source file='/disk/snap1.qcow2'/>"
            },
            # qemu-img invalid json
            {
                "code": 0,
                "stdout": "invalid json"
            }
        ]

if __name__ == "__main__":
    unittest.main()
