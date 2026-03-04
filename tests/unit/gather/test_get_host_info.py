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
from unittest import mock
from gather.get_host_info import HostHypervisorCollector

class TestHostHypervisorCollector(unittest.TestCase):

    def test_collect_all_basic(self):
        collector = HostHypervisorCollector()
        def fake_run_virsh_cmd(cmd):
            return None
        with mock.patch.object(
            collector, "run_virsh_cmd", side_effect=fake_run_virsh_cmd
        ):
            collector.collect_all()
