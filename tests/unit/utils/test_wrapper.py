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
