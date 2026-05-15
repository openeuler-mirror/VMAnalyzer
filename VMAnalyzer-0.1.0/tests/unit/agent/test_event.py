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

    def test_dom_event_callback_crashed_removes_vm(self):
        from agent import vm as vm_module
        from utils import constants as const
        ev = event.VMEventLoopNative("qemu:///system")

        mock_conn = mock.MagicMock()
        mock_dom = mock.MagicMock()
        test_id = 7001
        mock_dom.ID.return_value = test_id
        mock_dom.UUIDString.return_value = 'aaaa-bbbb-cccc'
        mock_dom.name.return_value = 'test-crash-vm'

        vm_factory = vm_module.VMFactory()
        vm_factory.add_vm(test_id, {'uuid': 'aaaa-bbbb-cccc', 'name': 'test-crash-vm'})
        self.assertIn(test_id, vm_factory.vms)

        ev.dom_event_callback(mock_conn, mock_dom,
                              const.VM_DOMAIN_EVENT_CRASHED, 0, None)
        self.assertNotIn(test_id, vm_factory.vms)

    def test_conn_close_callback_sets_run_false(self):
        ev = event.VMEventLoopNative("qemu:///system")
        mock_conn = mock.MagicMock()
        mock_conn.getURI.return_value = "qemu:///system"

        event.run = True
        ev.conn_close_callback(mock_conn, 0, None)
        self.assertFalse(event.run)
        event.run = True  # restore

    def test_get_uri(self):
        uri = "qemu:///system"
        ev = event.VMEventLoopNative(uri)
        self.assertEqual(ev.get_uri(), uri)

if __name__ == "__main__":
    unittest.main()
