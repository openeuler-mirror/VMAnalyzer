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
import time
import threading
import sys
import os

from utils.timer import RepeatedTimer


class TestRepeatedTimer(unittest.TestCase):
    """Documentation for this component."""

    def setUp(self):
        """Documentation for this component."""
        # English comment for this block.
        self.call_count = 0
        self.count_lock = threading.Lock()
        # English comment for this block.
        self.test_done = threading.Event()

    def test_function(self):
        """Documentation for this component."""
        with self.count_lock:
            self.call_count += 1
        # English comment for this block.
        if self.call_count >= 3:
            self.test_done.set()

    def test_init_auto_start(self):
        """Documentation for this component."""
        # English comment for this block.
        rt = RepeatedTimer(10, self.test_function)
        try:
            # English comment for this block.
            self.assertEqual(rt.is_running, True)
        finally:
            # English comment for this block.
            rt.stop()

    def test_function_executed_repeatedly(self):
        """Documentation for this component."""
        interval = 0.1  # English comment for this block.
        expected_calls = 3  # English comment for this block.

        # English comment for this block.
        rt = RepeatedTimer(interval, self.test_function)
        try:
            # English comment for this block.
            self.test_done.wait(timeout=1.0)
            # English comment for this block.
            with self.count_lock:
                self.assertEqual(self.call_count, expected_calls)
        finally:
            rt.stop()

    def test_stop_stops_timer(self):
        """Documentation for this component."""
        interval = 0.1
        # English comment for this block.
        rt = RepeatedTimer(interval, self.test_function)
        try:
            # English comment for this block.
            time.sleep(0.15)
            # English comment for this block.
            rt.stop()
            # English comment for this block.
            with self.count_lock:
                current_count = self.call_count
            # English comment for this block.
            time.sleep(0.2)
            # English comment for this block.
            with self.count_lock:
                self.assertEqual(self.call_count, current_count)
            # English comment for this block.
            self.assertEqual(rt.is_running, False)
        finally:
            rt.stop()

    def test_start_when_running(self):
        """Documentation for this component."""
        interval = 0.1
        rt = RepeatedTimer(interval, self.test_function)
        try:
            # English comment for this block.
            original_next_call = rt.next_call
            # English comment for this block.
            rt.start()
            # English comment for this block.
            self.assertEqual(rt.next_call, original_next_call)
            # English comment for this block.
            self.assertEqual(rt.is_running, True)
        finally:
            rt.stop()

    def tearDown(self):
        """Documentation for this component."""
        # English comment for this block.
        self.test_done.clear()
        self.call_count = 0


if __name__ == '__main__':
    unittest.main(verbosity=2)
