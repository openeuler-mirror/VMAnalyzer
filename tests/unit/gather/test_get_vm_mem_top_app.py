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

        # 场景4：JSON解析失败，返回无效字符串
        with patch.object(self.collector, "_exec_virsh_cmd") as mock_exec, patch.object(logger, "error") as mock_log_err:
            mock_exec.return_value = "invalid json string"
            result = self.collector.get_vm_mem_topn(test_vm)
            self.assertIsNone(result)
            self.assertIn(f"VM {test_vm} QGA返回解析失败", mock_log_err.call_args[0][0])

    def test_format_process_data(self):
        """测试format_process_data：覆盖正常格式/嵌套process-info/字段缺失所有兼容场景"""
        # 场景1：正常格式数据，字段完整
        raw_normal = [
            {
                "process-id": "123",
                "process-info": {
                    "user": "root",
                    "cpu-util": "10.5",
                    "mem-util": "20.3",
                    "open-files": "100",
                    "cmd-name": "java\n-Dtest"
                }
            }
        ]
        formatted_normal = self.collector.format_process_data(raw_normal)
        self.assertEqual(formatted_normal[0], {
            "process_id": "123",
            "user": "root",
            "cpu_util": "10.5",
            "mem_util": "20.3",
            "open_files": "100",
            "cmd_name": "java-Dtest"  # 验证\n被替换
        })

        # 场景2：异常格式
        raw_nested = [
            {
                "process-id": "456",
                "process-info": {
                    "process-info": {
                        "user": "nginx",
                        "cpu-util": "0.5",
                        "mem-util": "5.2",
                        "open-files": "50",
                        "cmd-name": "nginx"
                    }
                }
            }
        ]
        formatted_nested = self.collector.format_process_data(raw_nested)
        self.assertEqual(formatted_nested[0]["user"], "nginx")
        self.assertEqual(formatted_nested[0]["cmd_name"], "nginx")

        # 场景3：键**不存在**，触发get默认值
        raw_key_missing = [
            {
                # 缺失process-id键
                "process-info": {
                    # 缺失user/cpu-util/mem-util/open-files/cmd-name键
                }
            }
        ]
        formatted_key_missing = self.collector.format_process_data(raw_key_missing)
        self.assertEqual(formatted_key_missing[0], {
            "process_id": "未知",
            "user": "未知",
            "cpu_util": "0",
            "mem_util": "0",
            "open_files": "N/A",
            "cmd_name": "未知"
        })

        # 场景4：键**存在但值为空**，验证空值处理逻辑
        raw_value_empty = [
            {
                "process-id": "",
                "process-info": {
                    "user": "",
                    "cpu-util": "",
                    "mem-util": "",
                    "open-files": "",
                    "cmd-name": ""
                }
            }
        ]
        formatted_value_empty = self.collector.format_process_data(raw_value_empty)
        self.assertEqual(formatted_value_empty[0], {
            "process_id": "",
            "user": "",
            "cpu_util": "",
            "mem_util": "",
            "open_files": "",
            "cmd_name": ""
        })

    def test_collect_all_vms_data(self):
        mock_collect_time = "2026-02-06 10:00:00"
        with patch("gather.get_vm_mem_top_app.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime.strptime(mock_collect_time, "%Y-%m-%d %H:%M:%S")
            mock_datetime.strftime = datetime.strftime

            # 场景1：当前无运行中的VM
            with patch.object(self.collector, "get_running_vms") as mock_get_vms:
                mock_get_vms.return_value = []
                self.collector.collect_all_vms_data()
                self.assertEqual(self.collector.collect_data["collect_time"], mock_collect_time)
                self.assertEqual(self.collector.collect_data["running_vm_count"], 0)
                self.assertEqual(self.collector.collect_data["vm_list"], {})

            self.collector.collect_data = {"collect_time": "", "running_vm_count": 0, "vm_list": {}}
            # 场景2：单个VM采集成功
            with patch.object(self.collector, "get_running_vms") as mock_get_vms:
                mock_get_vms.return_value = ["vm-web01"]
                # 模拟get_vm_mem_topn返回正常数据
                mock_raw_data = [{"process-id": "123", "process-info": {"user": "root"}}]
                with patch.object(self.collector, "get_vm_mem_topn") as mock_get_topn:
                    mock_get_topn.return_value = mock_raw_data
                    self.collector.collect_all_vms_data()
                    self.assertEqual(self.collector.collect_data["running_vm_count"], 1)
                    self.assertIn("vm-web01", self.collector.collect_data["vm_list"])
                    self.assertEqual(self.collector.collect_data["vm_list"]["vm-web01"]["status"], "采集成功")
                    self.assertEqual(self.collector.collect_data["vm_list"]["vm-web01"]["top_n"], self.top_n)

            self.collector.collect_data = {"collect_time": "", "running_vm_count": 0, "vm_list": {}}
            # 场景3：单个VM采集失败（get_vm_mem_topn返回None）
            with patch.object(self.collector, "get_running_vms") as mock_get_vms:
                mock_get_vms.return_value = ["vm-db01"]
                with patch.object(self.collector, "get_vm_mem_topn") as mock_get_topn:
                    mock_get_topn.return_value = None
                    self.collector.collect_all_vms_data()
                    self.assertEqual(self.collector.collect_data["vm_list"]["vm-db01"]["status"], "采集失败")
                    self.assertEqual(self.collector.collect_data["vm_list"]["vm-db01"]["process_list"], [])

            self.collector.collect_data = {"collect_time": "", "running_vm_count": 0, "vm_list": {}}
            # 场景4：多个VM，部分成功部分失败
            with patch.object(self.collector, "get_running_vms") as mock_get_vms:
                mock_get_vms.return_value = ["vm-web01", "vm-db01"]
                with patch.object(self.collector, "get_vm_mem_topn") as mock_get_topn:
                    # 第一个VM成功，第二个失败
                    mock_get_topn.side_effect = [mock_raw_data, None]
                    self.collector.collect_all_vms_data()
                    self.assertEqual(self.collector.collect_data["running_vm_count"], 2)
                    self.assertEqual(self.collector.collect_data["vm_list"]["vm-web01"]["status"], "采集成功")
                    self.assertEqual(self.collector.collect_data["vm_list"]["vm-db01"]["status"], "采集失败")

    def test_save_collect_data(self):
        mock_collect_data = {
            "collect_time": "2026-02-06 10:00:00",
            "running_vm_count": 1,
            "vm_list": {
                "vm-web01": {
                    "status": "采集成功",
                    "process_list": [{"process_id": "123", "user": "root"}],
                    "top_n": 5
                }
            }
        }
        self.collector.collect_data = mock_collect_data

        mock_file_time = "20260206_100000"
        with patch("gather.get_vm_mem_top_app.datetime") as mock_datetime:
            mock_now = datetime.strptime("2026-02-06 10:00:00", "%Y-%m-%d %H:%M:%S")
            mock_datetime.now.return_value = mock_now
            mock_datetime.strftime = datetime.strftime

            self.collector.save_collect_data()

            test_file = f"vm_mem_topn_{mock_file_time}.json"
            test_file_path = os.path.join(self.test_out_dir, test_file)
            self.assertTrue(os.path.exists(test_file_path))

            with open(test_file_path, "r", encoding="utf-8") as f:
                save_data = json.load(f)
            self.assertEqual(save_data, mock_collect_data)

        with patch("builtins.open", side_effect=PermissionError("no write permission")), \
                patch.object(logger, "error") as mock_log_err:
            self.collector.save_collect_data()
            mock_log_err.assert_called_with("保存数据失败：no write permission")

    def test_parse_args(self):
        # 场景1：使用默认参数，无命令行入参
        with patch("sys.argv", ["get_vm_mem_top_app.py"]):
            args = parse_args()
            self.assertEqual(args.top_n, 5)
            self.assertEqual(args.poll_interval, 60)
            self.assertEqual(args.output_dir, "./vm_mem_topn_data")

        # 场景2：自定义所有参数
        with patch("sys.argv", [
            "get_vm_mem_top_app.py",
            "--top-n", "10",
            "--poll-interval", "30",
            "--output-dir", "/data/vm_mon/mem_topn"
        ]):
            args = parse_args()
            self.assertEqual(args.top_n, 10)
            self.assertEqual(args.poll_interval, 30)
            self.assertEqual(args.output_dir, "/data/vm_mon/mem_topn")

    def test_main(self):
        with patch("gather.get_vm_mem_top_app.parse_args") as mock_parse, \
                patch("gather.get_vm_mem_top_app.VMMemTopNCollector") as mock_collector_cls:
            mock_args = MagicMock()
            mock_args.top_n = 5
            mock_args.poll_interval = 60
            mock_args.output_dir = "./vm_mem_topn_data"
            mock_parse.return_value = mock_args

            main()

            mock_parse.assert_called_once()
            mock_collector_cls.assert_called_once_with(
                top_n=5,
                poll_interval=60,
                output_dir="./vm_mem_topn_data"
            )
            mock_collector_cls.return_value.start_polling.assert_called_once()

    def test_start_polling(self):
        with patch.object(self.collector, "collect_all_vms_data") as mock_collect, \
                patch.object(self.collector, "save_collect_data") as mock_save, \
                patch("time.sleep") as mock_sleep, \
                patch.object(logger, "info") as mock_log_info:
            mock_sleep.side_effect = KeyboardInterrupt()
            try:
                self.collector.start_polling()
            except KeyboardInterrupt:
                pass

            mock_collect.assert_called_once()
            mock_save.assert_called_once()
            mock_sleep.assert_called_once_with(self.poll_interval)
            all_logs = "".join([call[0][0] for call in mock_log_info.call_args_list])
            self.assertIn("用户终止采集，程序退出", all_logs)

        with patch.object(self.collector, "collect_all_vms_data") as mock_collect, \
                patch.object(self.collector, "save_collect_data") as mock_save, \
                patch("time.sleep"), \
                patch.object(logger, "error") as mock_log_err:
            mock_collect.side_effect = RuntimeError("poll error")
            try:
                self.collector.start_polling()
            except RuntimeError:
                pass

            mock_log_err.assert_called_with("轮询采集异常：poll error")

if __name__ == "__main__":
    unittest.main(verbosity=2)
