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
import os
import json
import shutil
import subprocess
from datetime import datetime
from unittest.mock import patch, MagicMock

from gather.get_vm_mem_top_app import VMMemTopNCollector, logger, parse_args, main

class TestGetVMMemTopApp(unittest.TestCase):
    """VM内存TopN进程采集模块单元测试"""
    def setUp(self):
        self.top_n = 5
        self.poll_interval = 10
        self.test_out_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "temp", "test_vm_mem_topn"
        )
        self.collector = VMMemTopNCollector(
            top_n=self.top_n,
            poll_interval=self.poll_interval,
            output_dir=self.test_out_dir
        )

    def tearDown(self):
        temp_root = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "temp"
        )
        if os.path.exists(temp_root):
            shutil.rmtree(temp_root)

    def test_init_and_init_output_dir(self):
        self.assertEqual(self.collector.top_n, self.top_n)
        self.assertEqual(self.collector.poll_interval, self.poll_interval)
        self.assertEqual(self.collector.output_dir, self.test_out_dir)
        self.assertEqual(self.collector.collect_data, {
            "collect_time": "",
            "running_vm_count": 0,
            "vm_list": {}
        })
        self.assertTrue(os.path.exists(self.test_out_dir))

    def test__exec_virsh_cmd_all_scenarios(self):
        test_cmd = "virsh list --name"

        class TestableCollector(self.collector.__class__):
            def call_exec_virsh_cmd(self, cmd):
                return super()._exec_virsh_cmd(cmd)

        self.collector = TestableCollector()

        with patch("subprocess.run") as mock_subproc, patch.object(logger, "info") as mock_log_info, \
                patch.object(logger, "error") as mock_log_err:
            # 场景1：命令执行成功，返回非空输出
            mock_res = MagicMock()
            mock_res.stdout.strip.return_value = "vm1 vm2"
            mock_subproc.return_value = mock_res
            result = self.collector.call_exec_virsh_cmd(test_cmd)
            self.assertEqual(result, "vm1 vm2")
            mock_log_info.assert_called_with(f"执行命令：{test_cmd}")
            mock_log_err.assert_not_called()

            # 场景2：命令执行失败（CalledProcessError）
            mock_subproc.side_effect = subprocess.CalledProcessError(
                returncode=1, cmd=test_cmd, stderr="connect failed"
            )
            result = self.collector.call_exec_virsh_cmd(test_cmd)
            self.assertIsNone(result)
            mock_log_err.assert_called_with(f"命令执行失败：{test_cmd}，错误：connect failed")

            # 场景3：命令执行超时（TimeoutExpired）
            mock_subproc.side_effect = subprocess.TimeoutExpired(cmd=test_cmd, timeout=30)
            result = self.collector.call_exec_virsh_cmd(test_cmd)
            self.assertIsNone(result)
            mock_log_err.assert_called_with(f"命令执行超时：{test_cmd}（超过30秒）")

            # 场景4：通用异常（如权限不足）
            mock_subproc.side_effect = Exception("permission denied")
            result = self.collector.call_exec_virsh_cmd(test_cmd)
            self.assertIsNone(result)
            mock_log_err.assert_called_with(f"命令执行异常：{test_cmd}，错误：permission denied")

            # 场景5：命令成功但无输出，返回None
            mock_res.stdout.strip.return_value = ""
            mock_subproc.side_effect = None
            result = self.collector.call_exec_virsh_cmd(test_cmd)
            self.assertIsNone(result)

    def test_get_running_vms(self):
        # 场景1：有运行VM，返回非空列表
        with patch.object(self.collector, "_exec_virsh_cmd") as mock_exec:
            mock_exec.return_value = "vm-db01 vm-web01 vm-cache01"
            vms = self.collector.get_running_vms()
            self.assertEqual(vms, ["vm-db01", "vm-web01", "vm-cache01"])
            mock_exec.assert_called_once_with("virsh list --name | grep -v '^$'")

        # 场景2：无运行VM，返回空列表
        with patch.object(self.collector, "_exec_virsh_cmd") as mock_exec:
            mock_exec.return_value = None
            vms = self.collector.get_running_vms()
            self.assertEqual(vms, [])

    def test_get_vm_mem_topn_all_scenarios(self):
        test_vm = "vm-db01"
        mock_qga_resp = "{\"return\": [{\"process-id\": \"123\", \"process-info\": {\"user\": \"root\"}}]}"
        # 场景1：采集成功，正常返回数据
        with patch.object(self.collector, "_exec_virsh_cmd") as mock_exec, patch.object(logger, "error") as mock_log_err:
            mock_exec.return_value = mock_qga_resp
            result = self.collector.get_vm_mem_topn(test_vm)
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 1)
            expected_qga_params = json.dumps({
                "execute": "guest-get-memtopn-status",
                "arguments": {"memtopn-num": str(self.top_n)}
            })
            mock_exec.assert_called_once_with(f"virsh qemu-agent-command {test_vm} '{expected_qga_params}'")
            mock_log_err.assert_not_called()

        # 场景2：命令无返回数据，采集失败
        with patch.object(self.collector, "_exec_virsh_cmd") as mock_exec, patch.object(logger, "error") as mock_log_err:
            mock_exec.return_value = None
            result = self.collector.get_vm_mem_topn(test_vm)
            self.assertIsNone(result)
            mock_log_err.assert_called_with(f"VM {test_vm} 内存TopN信息采集失败：无返回数据")

        # 场景3：QGA返回无return字段，格式异常
        with patch.object(self.collector, "_exec_virsh_cmd") as mock_exec, patch.object(logger, "error") as mock_log_err:
            mock_exec.return_value = "{\"error\": \"unknown command\"}"
            result = self.collector.get_vm_mem_topn(test_vm)
            self.assertIsNone(result)
            mock_log_err.assert_called_with(f"VM {test_vm} QGA返回格式异常：{{\"error\": \"unknown command\"}}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
