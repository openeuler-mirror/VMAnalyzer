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
import logging
import sys
import os
from io import StringIO

from utils.wrapper import singleton


class TestSingletonDecorator(unittest.TestCase):
    """针对singleton装饰器的单元测试用例"""

    def setUp(self):
        """测试前初始化：重置日志捕获器，定义测试用的类"""
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG) 
        self.log_buffer = StringIO()
        self.log_handler = logging.StreamHandler(self.log_buffer)
        self.log_handler.setLevel(logging.DEBUG)
        # 添加日志格式
        formatter = logging.Formatter("%(levelname)s: %(message)s")
        self.log_handler.setFormatter(formatter)
        self.logger.addHandler(self.log_handler)

        # 定义被装饰的测试类（带参数初始化）
        @singleton
        class TestClass:
            def __init__(self, name, age=18):
                self.name = name
                self.age = age

        # 定义另一个测试类（验证不同类单例互不干扰）
        @singleton
        class AnotherTestClass:
            def __init__(self, value):
                self.value = value

        self.TestClass = TestClass
        self.AnotherTestClass = AnotherTestClass

    def tearDown(self):
        """测试后清理：移除日志处理器，关闭内存流"""
        self.logger.removeHandler(self.log_handler)
        self.log_handler.close()
        self.log_buffer.close()

    def test_singleton_return_same_instance(self):
        """测试多次实例化返回同一个对象"""
        # 第一次实例化
        instance1 = self.TestClass("test", age=20)
        # 第二次实例化（参数不同，验证仍返回第一个实例）
        instance2 = self.TestClass("another", age=30)

        # 验证两个实例是同一个对象（内存地址相同）
        self.assertIs(instance1, instance2)
        # 验证实例属性是第一次初始化的参数
        self.assertEqual(instance1.name, "test")
        self.assertEqual(instance1.age, 20)

    def test_singleton_parameter_passing(self):
        """验证初始化参数能正确传递给类"""
        instance = self.TestClass("张三", age=25)
        # 验证参数正确赋值给实例属性
        self.assertEqual(instance.name, "张三")
        self.assertEqual(instance.age, 25)

    def test_different_class_singleton_isolated(self):
        """测试不同类使用装饰器，单例互不干扰"""
        # 实例化第一个类
        test_instance = self.TestClass("test")
        # 实例化第二个类
        another_instance = self.AnotherTestClass(100)

        # 验证两个实例不是同一个对象
        self.assertIsNot(test_instance, another_instance)
        # 验证第二个类的单例属性正确
        self.assertEqual(another_instance.value, 100)

    def test_singleton_log_output(self):
        """验证debug日志输出"""
        # 清空日志缓冲区
        self.log_buffer.seek(0)
        self.log_buffer.truncate()

        # 重新定义一个简单的被装饰类，触发日志输出
        @singleton
        class LogTestClass:
            def __init__(self):
                pass

        # 实例化触发装饰器的日志输出
        LogTestClass()

        # 获取并解析日志内容
        self.log_buffer.seek(0)
        log_output = self.log_buffer.read().strip()
        
        # 验证日志包含装饰器输出的args和kwargs（第一次调用时args=(), kwargs={}）
        self.assertIn("DEBUG: () {}", log_output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
