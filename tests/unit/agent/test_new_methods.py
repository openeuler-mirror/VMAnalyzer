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
