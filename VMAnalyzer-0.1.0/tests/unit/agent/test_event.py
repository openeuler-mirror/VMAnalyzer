#!/usr/bin/env python
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
import mock
from agent import event
try:
    import libvirt
except ImportError:
    pass


class TestVMEventLoopNative(unittest.TestCase):
    """
    该类用于对 `VMEventLoopNative` 类进行单元测试。

    继承自 `unittest.TestCase`，主要目的是验证 `VMEventLoopNative` 类的
    `start` 方法是否能正确调用 `libvirt` 库中的 `virEventRegisterDefaultImpl` 函数。
    """
    def test_start(self):
        with mock.patch.object(
                libvirt, "virEventRegisterDefaultImpl"
        ) as mock_register:
            ev = event.VMEventLoopNative("qemu:///system")
            ev.start()
            self.assertTrue(mock_register.called)

if __name__ == "__main__":
    unittest.main()
