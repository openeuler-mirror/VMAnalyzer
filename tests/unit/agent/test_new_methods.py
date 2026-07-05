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

"""Documentation for this component."""

import json
import os
import tempfile
import unittest

from unittest import mock

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
    """Documentation for this component."""
    factory = vm.VMFactory()
    if _TEST_VM_ID not in factory.vms:
        factory.add_vm(_TEST_VM_ID, _TEST_VM_INFO)
    return factory


# ── TestCheckConnection ───────────────────────────────────────────────────────

class TestCheckConnection(unittest.TestCase):
    """Documentation for this component."""

    def setUp(self):
        self.vm_factory = _ensure_test_vm()
        # English comment for this block.
        self.vm_storage = storage.VMStatsRedisStorage(self.vm_factory, "cpuUsage")

    def test_returns_true_when_ping_succeeds(self):
        """Documentation for this component."""
        with mock.patch.object(self.vm_storage.sr, "ping", return_value=True):
            ok, msg = self.vm_storage.check_connection()
        self.assertTrue(ok)
        self.assertIsNone(msg)

    def test_returns_false_when_ping_raises(self):
        """Documentation for this component."""
        with mock.patch.object(
            self.vm_storage.sr, "ping",
            side_effect=Exception("Connection refused")
        ):
            ok, msg = self.vm_storage.check_connection()
        self.assertFalse(ok)
        self.assertIsInstance(msg, str)
        self.assertIn("Connection refused", msg)

    def test_error_message_contains_host_and_port(self):
        """Documentation for this component."""
        with mock.patch.object(
            self.vm_storage.sr, "ping",
            side_effect=Exception("timeout")
        ):
            _, msg = self.vm_storage.check_connection()
        # English comment for this block.
        self.assertIn("localhost", msg)
        self.assertIn("6379", msg)

# ── TestCleanupOldStats ───────────────────────────────────────────────────────

class TestCleanupOldStats(unittest.TestCase):
    """Documentation for this component."""

    def setUp(self):
        self.vm_factory = _ensure_test_vm()
        self.vm_storage = storage.VMStatsRedisStorage(self.vm_factory, "cpuUsage")

    def test_calls_zremrangebyscore_with_correct_key(self):
        """Documentation for this component."""
        with mock.patch.object(
            self.vm_storage.sr, "zremrangebyscore", return_value=3
        ) as mock_zrem:
            self.vm_storage.cleanup_old_stats(_TEST_VM_ID, retention_seconds=3600)

        mock_zrem.assert_called_once()
        key, lo, _ = mock_zrem.call_args[0]
        self.assertEqual(key, _TEST_VM_INFO["uuid"])
        self.assertEqual(lo, "-inf")

    def test_cutoff_is_before_now(self):
        """Documentation for this component."""
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
        # English comment for this block.
        self.assertGreater(cutoff, before - 3601)
        self.assertLess(cutoff, after - 3599)

    def test_skips_unknown_vm(self):
        """Documentation for this component."""
        with mock.patch.object(
            self.vm_storage.sr, "zremrangebyscore"
        ) as mock_zrem:
            self.vm_storage.cleanup_old_stats(vm_id=99999, retention_seconds=3600)
        mock_zrem.assert_not_called()

    def test_handles_redis_exception_gracefully(self):
        """Documentation for this component."""
        with mock.patch.object(
            self.vm_storage.sr, "zremrangebyscore",
            side_effect=Exception("connection lost")
        ):
            # English comment for this block.
            try:
                self.vm_storage.cleanup_old_stats(_TEST_VM_ID, retention_seconds=60)
            except Exception:  # noqa: BLE001
                self.fail("Operation message")

# ── TestVMAnalyzersFileView ───────────────────────────────────────────────────

class TestVMAnalyzersFileView(unittest.TestCase):
    """Documentation for this component."""

    _SAMPLE = [
        {"vm-a": {"Current_cpu_utilization": 0.35, "TimeStamp": 1700000000}},
        {"vm-a": {"Current_cpu_utilization": 0.42, "TimeStamp": 1700000001}},
    ]

    def test_creates_output_file(self):
        """Documentation for this component."""
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            path = f.name
        os.unlink(path)   # English comment for this block.
        try:
            fv = view.VMAnalyzersFileView(path)
            fv.output(self._SAMPLE)
            self.assertTrue(os.path.exists(path))
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_writes_one_line_per_record(self):
        """Documentation for this component."""
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
        """Documentation for this component."""
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
        """Documentation for this component."""
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
        """Documentation for this component."""
        fv = view.VMAnalyzersFileView("/nonexistent_dir/test.jsonl")
        try:
            fv.output(self._SAMPLE)
        except Exception:  # noqa: BLE001
            self.fail("Operation message")

    def test_creates_parent_directory(self):
        """Documentation for this component."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "subdir", "out.jsonl")
            fv = view.VMAnalyzersFileView(path)
            fv.output(self._SAMPLE)
            self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
