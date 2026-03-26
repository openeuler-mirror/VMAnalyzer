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
from unittest.mock import patch, MagicMock
from io import StringIO

from gather import getlibver

class TestGetLibVer(unittest.TestCase):

    # =========================
    # createConnection
    # =========================
    @patch("gather.getlibver.libvirt.openReadOnly")
    def test_create_connection_success(self, mock_open):
        mock_conn = MagicMock()
        mock_open.return_value = mock_conn
        result = getlibver.createConnection("qemu:///system")
        self.assertEqual(result, mock_conn)
        mock_open.assert_called_once_with("qemu:///system")

    @patch("gather.getlibver.libvirt.openReadOnly")
    def test_create_connection_fail(self, mock_open):
        mock_open.return_value = None
        result = getlibver.createConnection("qemu:///system")
        self.assertIsNone(result)

    # =========================
    # closeConnection
    # =========================
    def test_close_connection_success(self):
        mock_conn = MagicMock()
        getlibver.closeConnection(mock_conn)
        mock_conn.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()
