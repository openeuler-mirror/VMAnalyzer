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
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG) 
        self.log_buffer = StringIO()
        self.log_handler = logging.StreamHandler(self.log_buffer)
        self.log_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s: %(message)s")
        self.log_handler.setFormatter(formatter)
        self.logger.addHandler(self.log_handler)

        @singleton
        class TestClass:
            def __init__(self, name, age=18):
                self.name = name
                self.age = age

        @singleton
        class AnotherTestClass:
            def __init__(self, value):
                self.value = value

        self.TestClass = TestClass
        self.AnotherTestClass = AnotherTestClass

    def tearDown(self):
        self.logger.removeHandler(self.log_handler)
        self.log_handler.close()
        self.log_buffer.close()

    def test_singleton_return_same_instance(self):
        instance1 = self.TestClass("test", age=20)
        instance2 = self.TestClass("another", age=30)

        self.assertIs(instance1, instance2)
        self.assertEqual(instance1.name, "test")
        self.assertEqual(instance1.age, 20)

    def test_singleton_parameter_passing(self):
        instance = self.TestClass("张三", age=25)
        self.assertEqual(instance.name, "张三")
        self.assertEqual(instance.age, 25)

    def test_different_class_singleton_isolated(self):
        test_instance = self.TestClass("test")
        another_instance = self.AnotherTestClass(100)

        self.assertIsNot(test_instance, another_instance)
        self.assertEqual(another_instance.value, 100)
