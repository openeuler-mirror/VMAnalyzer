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
        """每个测试用例执行前的初始化：重置计数器和事件"""
        # 用线程安全的计数器记录函数调用次数（避免多线程竞争）
        self.call_count = 0
        self.count_lock = threading.Lock()
        # 用于标记测试结束的事件（避免无限等待）
        self.test_done = threading.Event()

    def test_function(self):
        """被定时器调用的测试函数：安全增加计数器"""
        with self.count_lock:
            self.call_count += 1
        # 当调用次数达到预期时，触发结束事件
        if self.call_count >= 3:
            self.test_done.set()

    def test_init_auto_start(self):
        """测试初始化时是否自动启动定时器"""
        # 初始化定时器
        rt = RepeatedTimer(10, self.test_function)
        try:
            # 验证初始化后is_running为True
            self.assertEqual(rt.is_running, True)
        finally:
            # 清理：停止定时器，避免残留线程
            rt.stop()

    def test_function_executed_repeatedly(self):
        """验证函数按指定间隔重复执行"""
        interval = 0.1  # 短间隔，加快测试速度
        expected_calls = 3  # 预期调用3次

        # 初始化定时器
        rt = RepeatedTimer(interval, self.test_function)
        try:
            # 等待：要么达到预期调用次数，要么超时
            self.test_done.wait(timeout=1.0)
            # 验证实际调用次数等于预期
            with self.count_lock:
                self.assertEqual(self.call_count, expected_calls)
        finally:
            rt.stop()

    def test_stop_stops_timer(self):
        """验证stop方法能停止定时器，函数不再被调用"""
        interval = 0.1
        # 初始化定时器并执行1次后停止
        rt = RepeatedTimer(interval, self.test_function)
        try:
            # 等待第一次调用完成（0.15秒 > 0.1秒间隔）
            time.sleep(0.15)
            # 停止定时器
            rt.stop()
            # 记录当前调用次数
            with self.count_lock:
                current_count = self.call_count
            # 再等待足够时间（0.2秒），验证函数不再被调用
            time.sleep(0.2)
            # 再次检查调用次数，确认未增加
            with self.count_lock:
                self.assertEqual(self.call_count, current_count)
            # 验证is_running状态为False
            self.assertEqual(rt.is_running, False)
        finally:
            rt.stop()

    def test_start_when_running(self):
        """验证已运行时调用start无副作用"""
        interval = 0.1
        rt = RepeatedTimer(interval, self.test_function)
        try:
            # 记录初始的next_call时间
            original_next_call = rt.next_call
            # 已运行时再次调用start
            rt.start()
            # 验证next_call未被修改
            self.assertEqual(rt.next_call, original_next_call)
            # 验证is_running仍为True
            self.assertEqual(rt.is_running, True)
        finally:
            rt.stop()

    def tearDown(self):
        """每个测试用例执行后的清理：确保定时器停止"""
        # 重置事件和计数器
        self.test_done.clear()
        self.call_count = 0


if __name__ == '__main__':
    unittest.main(verbosity=2)
