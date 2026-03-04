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

mock_libvirt_module = MagicMock()
mock_libvirt_qemu_module = MagicMock()

import sys
sys.modules['libvirt'] = mock_libvirt_module
sys.modules['libvirt_qemu'] = mock_libvirt_qemu_module

mock_libvirt_module.open = MagicMock()
mock_libvirt_module.LibvirtError = Exception
mock_libvirt_qemu_module.qemuAgentCommand = MagicMock()

TEST_MODULE = __name__

class TestGetVMProcDishstats(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main(verbosity=2)
