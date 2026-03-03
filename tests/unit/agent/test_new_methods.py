#!/usr/bin/env python
# _*_coding: utf-8 _*_
#######################################################################################
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
#######################################################################################

"""test_new_methods.py — 单元测试：本轮新增的 agent 方法和视图类。

覆盖范围：
  VMStatsRedisStorage.check_connection()  — Redis 连通性校验
  VMStatsRedisStorage.cleanup_old_stats() — Redis 历史数据清理
  VMAnalyzersFileView                     — JSON Lines 文件输出视图
"""

import json
import os
import tempfile
import unittest

import mock

from agent import storage
from agent import view
from agent import vm


_TEST_VM_ID = 7001
_TEST_VM_INFO = {
    "uuid": "aabbccdd-0000-0000-0000-111122223333",
    "name": "instance-test-new-methods",
    "cpu_util": 0.0,
}

def _ensure_test_vm():
    """将测试 VM 注入 VMFactory 单例（幂等）。"""
    factory = vm.VMFactory()
    if _TEST_VM_ID not in factory.vms:
        factory.add_vm(_TEST_VM_ID, _TEST_VM_INFO)
    return factory


# ── TestCheckConnection ───────────────────────────────────────────────────────

class TestCheckConnection(unittest.TestCase):
    """测试 VMStatsRedisStorage.check_connection()。"""

    def setUp(self):
        self.vm_factory = _ensure_test_vm()
        # 获取（或创建）单例存储实例
        self.vm_storage = storage.VMStatsRedisStorage(self.vm_factory, "cpuUsage")

    def test_returns_true_when_ping_succeeds(self):
        """Redis ping 成功时 check_connection 应返回 (True, None)。"""
        with mock.patch.object(self.vm_storage.sr, "ping", return_value=True):
            ok, msg = self.vm_storage.check_connection()
        self.assertTrue(ok)
        self.assertIsNone(msg)

    def test_returns_false_when_ping_raises(self):
        """Redis ping 抛出异常时应返回 (False, 包含错误信息的字符串)。"""
        with mock.patch.object(
            self.vm_storage.sr, "ping",
            side_effect=Exception("Connection refused")
        ):
            ok, msg = self.vm_storage.check_connection()
        self.assertFalse(ok)
        self.assertIsInstance(msg, str)
        self.assertIn("Connection refused", msg)

    def test_error_message_contains_host_and_port(self):
        """错误信息中应包含 Redis 服务器地址。"""
        with mock.patch.object(
            self.vm_storage.sr, "ping",
            side_effect=Exception("timeout")
        ):
            _, msg = self.vm_storage.check_connection()
        # config 默认 host=localhost, port=6379
        self.assertIn("localhost", msg)
        self.assertIn("6379", msg)

# ── TestCleanupOldStats ───────────────────────────────────────────────────────

class TestCleanupOldStats(unittest.TestCase):
    """测试 VMStatsRedisStorage.cleanup_old_stats()。"""

    def setUp(self):
        self.vm_factory = _ensure_test_vm()
        self.vm_storage = storage.VMStatsRedisStorage(self.vm_factory, "cpuUsage")

    def test_calls_zremrangebyscore_with_correct_key(self):
        """cleanup_old_stats 应以 VM UUID 为 key 调用 zremrangebyscore。"""
        with mock.patch.object(
            self.vm_storage.sr, "zremrangebyscore", return_value=3
        ) as mock_zrem:
            self.vm_storage.cleanup_old_stats(_TEST_VM_ID, retention_seconds=3600)

        mock_zrem.assert_called_once()
        key, lo, _ = mock_zrem.call_args[0]
        self.assertEqual(key, _TEST_VM_INFO["uuid"])
        self.assertEqual(lo, "-inf")

    def test_cutoff_is_before_now(self):
        """cutoff 时间戳应严格小于当前时间。"""
        import time
        captured_cutoff = []

        def fake_zrem(key, lo, hi):
            captured_cutoff.append(hi)
            return 0

        with mock.patch.object(self.vm_storage.sr, "zremrangebyscore",
                               side_effect=fake_zrem):
            before = time.time()
            self.vm_storage.cleanup_old_stats(_TEST_VM_ID, retention_seconds=3600)
            after = time.time()

        self.assertEqual(len(captured_cutoff), 1)
        cutoff = captured_cutoff[0]
        # cutoff = now - 3600，应在 (before-3600, after-3600) 范围内
        self.assertGreater(cutoff, before - 3601)
        self.assertLess(cutoff, after - 3599)

    def test_skips_unknown_vm(self):
        """未知 vm_id 时不应调用 Redis。"""
        with mock.patch.object(
            self.vm_storage.sr, "zremrangebyscore"
        ) as mock_zrem:
            self.vm_storage.cleanup_old_stats(vm_id=99999, retention_seconds=3600)
        mock_zrem.assert_not_called()

    def test_handles_redis_exception_gracefully(self):
        """Redis 出错时不应向上抛出异常。"""
        with mock.patch.object(
            self.vm_storage.sr, "zremrangebyscore",
            side_effect=Exception("connection lost")
        ):
            # 期望不抛出，仅记录日志
            try:
                self.vm_storage.cleanup_old_stats(_TEST_VM_ID, retention_seconds=60)
            except Exception:  # noqa: BLE001
                self.fail("cleanup_old_stats 不应向上抛出 Redis 异常")

# ── TestVMAnalyzersFileView ───────────────────────────────────────────────────

class TestVMAnalyzersFileView(unittest.TestCase):
    """测试 VMAnalyzersFileView 文件输出视图。"""

    _SAMPLE = [
        {"vm-a": {"Current_cpu_utilization": 0.35, "TimeStamp": 1700000000}},
        {"vm-a": {"Current_cpu_utilization": 0.42, "TimeStamp": 1700000001}},
    ]

    def test_creates_output_file(self):
        """output() 调用后目标文件应存在。"""
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            path = f.name
        os.unlink(path)   # 先删掉，让 FileView 自己创建
        try:
            fv = view.VMAnalyzersFileView(path)
            fv.output(self._SAMPLE)
            self.assertTrue(os.path.exists(path))
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_writes_one_line_per_record(self):
        """每条分析记录应写为一行 JSON。"""
        with tempfile.NamedTemporaryFile(
            mode="r", suffix=".jsonl", delete=False
        ) as f:
            path = f.name
        try:
            fv = view.VMAnalyzersFileView(path)
            fv.output(self._SAMPLE)
            with open(path, "r", encoding="utf-8") as f:
                lines = [l for l in f.read().splitlines() if l]
            self.assertEqual(len(lines), len(self._SAMPLE))
            for line in lines:
                self.assertIsInstance(json.loads(line), dict)
        finally:
            os.unlink(path)

    def test_appends_on_repeated_calls(self):
        """多次调用 output() 应追加写入，不覆盖。"""
        with tempfile.NamedTemporaryFile(
            mode="r", suffix=".jsonl", delete=False
        ) as f:
            path = f.name
        try:
            fv = view.VMAnalyzersFileView(path)
            fv.output(self._SAMPLE)
            fv.output(self._SAMPLE)
            with open(path, "r", encoding="utf-8") as f:
                lines = [l for l in f.read().splitlines() if l]
            self.assertEqual(len(lines), len(self._SAMPLE) * 2)
        finally:
            os.unlink(path)

    def test_cpu_utilization_formatted_as_percent(self):
        """输出中 Current_cpu_utilization 应被转换为百分比字符串。"""
        with tempfile.NamedTemporaryFile(
            mode="r", suffix=".jsonl", delete=False
        ) as f:
            path = f.name
        try:
            fv = view.VMAnalyzersFileView(path)
            fv.output(self._SAMPLE)
            with open(path, "r", encoding="utf-8") as f:
                first = json.loads(f.readline())
            cpu_val = list(first.values())[0]["Current_cpu_utilization"]
            self.assertIn("%", cpu_val)
        finally:
            os.unlink(path)

    def test_write_error_does_not_raise(self):
        """向不可写路径输出时，不应向上抛出异常。"""
        fv = view.VMAnalyzersFileView("/nonexistent_dir/test.jsonl")
        try:
            fv.output(self._SAMPLE)
        except Exception:  # noqa: BLE001
            self.fail("VMAnalyzersFileView.output 不应向上抛出写文件异常")

    def test_creates_parent_directory(self):
        """父目录不存在时应自动创建。"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "subdir", "out.jsonl")
            fv = view.VMAnalyzersFileView(path)
            fv.output(self._SAMPLE)
            self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
