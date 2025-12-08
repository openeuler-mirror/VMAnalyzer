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
import unittest
import mock
from agent import event
import libvirt

# test vm event loop native
class TestVMEventLoopNative(unittest.TestCase):
    def test_start(self):
        # Patch libvirt's event implementation registration
        with mock.patch.object(
            libvirt, 'virEventRegisterDefaultImpl'
        ) as mock_register:
            ev = event.VMEventLoopNative("qemu:///system")
            ev.start()
            # Verify that the default event implementation waas registered
            mock_register.assert_called()  # Prefer assert_called() over .called

if __name__ == "__main__":
    unittest.main()