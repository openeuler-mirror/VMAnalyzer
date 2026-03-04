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
    """针对RepeatedTimer类的单元测试用例"""
    def setUp(self):
        self.call_count = 0
        self.count_lock = threading.Lock()
        self.test_done = threading.Event()

    def test_function(self):
        with self.count_lock:
            self.call_count += 1
        if self.call_count >= 3:
            self.test_done.set()

    def test_init_auto_start(self):
        rt = RepeatedTimer(10, self.test_function)
        try:
            self.assertEqual(rt.is_running, True)
        finally:
            rt.stop()

    def test_function_executed_repeatedly(self):
        interval = 0.1
        rt = RepeatedTimer(interval, self.test_function)
        try:
            self.test_done.wait(timeout=1.0)
        finally:
            rt.stop()

    def tearDown(self):
        self.test_done.clear()
        self.call_count = 0
