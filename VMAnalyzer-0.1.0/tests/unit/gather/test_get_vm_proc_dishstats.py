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
import os
import json
import datetime
import unittest
from unittest.mock import MagicMock, patch, ANY
import pytest
import logging

# 1. Mock libvirt和libvirt_qemu模块
mock_libvirt_module = MagicMock()
mock_libvirt_qemu_module = MagicMock()

import sys
sys.modules['libvirt'] = mock_libvirt_module
sys.modules['libvirt_qemu'] = mock_libvirt_qemu_module

mock_libvirt_module.open = MagicMock()
mock_libvirt_module.LibvirtError = Exception
mock_libvirt_qemu_module.qemuAgentCommand = MagicMock()

# 2. 定义测试文件的模块名
TEST_MODULE = __name__

# 3. 定义完全匹配预期的Mock类
class MockStatsStorage:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        # 确保目录创建（兼容空目录）
        os.makedirs(output_dir, exist_ok=True)

    def save_stats_info(self, stats):
        # 获取当前时间并格式化（确保与测试mock一致）
        now = datetime.datetime.now()
        timestamp_str = now.strftime("%Y%m%d_%H%M%S")
        test_file = os.path.join(self.output_dir, f"diskstats_info_{timestamp_str}.json")
        # 写入文件
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False)
        # 输出日志
        self.logger.info(f"统计信息已保存到: {test_file}")
