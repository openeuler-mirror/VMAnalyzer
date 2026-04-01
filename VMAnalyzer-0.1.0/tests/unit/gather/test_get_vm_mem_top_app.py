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
        """测试前置：初始化实例，创建独立测试临时目录"""
        self.top_n = 5
        self.poll_interval = 10
        # 测试目录放在项目根temp下，与业务隔离，测试后自动清理
        self.test_out_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "temp", "test_vm_mem_topn"
        )
        # 初始化采集器实例
        self.collector = VMMemTopNCollector(
            top_n=self.top_n,
            poll_interval=self.poll_interval,
            output_dir=self.test_out_dir
        )

    def tearDown(self):
        """测试后置：清理所有测试临时目录，无残留"""
        temp_root = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "temp"
        )
        if os.path.exists(temp_root):
            shutil.rmtree(temp_root)

    def test_init_and_init_output_dir(self):
        """测试__init__和_init_output_dir：参数初始化+目录创建逻辑"""
        # 断言实例参数正确
        self.assertEqual(self.collector.top_n, self.top_n)
        self.assertEqual(self.collector.poll_interval, self.poll_interval)
        self.assertEqual(self.collector.output_dir, self.test_out_dir)
        # 断言初始采集数据结构正确
        self.assertEqual(self.collector.collect_data, {
            "collect_time": "",
            "running_vm_count": 0,
            "vm_list": {}
        })
        # 断言输出目录已创建
        self.assertTrue(os.path.exists(self.test_out_dir))

    def test__exec_virsh_cmd_all_scenarios(self):
        """测试私有方法_exec_virsh_cmd：覆盖成功/命令失败/超时/通用异常所有场景"""
        test_cmd = "virsh list --name"

        class TestableCollector(self.collector.__class__):
            def call_exec_virsh_cmd(self, cmd):
                # 子类合法访问父类受保护方法，静态检查无警告
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
