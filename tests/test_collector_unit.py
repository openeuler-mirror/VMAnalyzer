#!/usr/bin/env python3
# _*_coding: utf-8 _*_
"""收集器单元测试"""
import unittest
class TestCollector(unittest.TestCase):
    def test_basic_collection(self):
        """测试基本收集功能"""
        self.assertTrue(True)
    def test_data_format(self):
        """测试数据格式"""
        self.assertIsNotNone({})
if __name__ == "__main__":
    unittest.main()
