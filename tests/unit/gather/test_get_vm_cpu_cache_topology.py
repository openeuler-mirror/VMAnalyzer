#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
import subprocess

from gather import get_vm_cpu_cache_topology

class TestGetVmCpuCacheTopology(unittest.TestCase):

    # =========================
    # run_virsh_cmd
    # =========================
    @patch("gather.get_vm_cpu_cache_topology.subprocess.run")
    def test_run_virsh_cmd_success(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="xml data",
            stderr=""
        )
        result = get_vm_cpu_cache_topology.run_virsh_cmd(
            "virsh dumpxml vm1"
        )
        self.assertEqual(result, "xml data")

    @patch("gather.get_vm_cpu_cache_topology.subprocess.run")
    def test_run_virsh_cmd_fail(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="error"
        )
        result = get_vm_cpu_cache_topology.run_virsh_cmd(
            "virsh dumpxml vm1"
        )
        self.assertIsNone(result)

    @patch("gather.get_vm_cpu_cache_topology.subprocess.run")
    def test_run_virsh_cmd_timeout(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd="virsh",
            timeout=30
        )
        result = get_vm_cpu_cache_topology.run_virsh_cmd(
            "virsh dumpxml vm1"
        )
        self.assertIsNone(result)

    @patch("gather.get_vm_cpu_cache_topology.subprocess.run")
    def test_run_virsh_cmd_exception(self, mock_run):
        mock_run.side_effect = Exception("boom")
        result = get_vm_cpu_cache_topology.run_virsh_cmd(
            "virsh dumpxml vm1"
        )
        self.assertIsNone(result)

    # =========================
    # get_domain_xml
    # =========================
    @patch(
        "gather.get_vm_cpu_cache_topology.run_virsh_cmd"
    )
    def test_get_domain_xml(self, mock_run):
        mock_run.return_value = "<xml/>"
        result = get_vm_cpu_cache_topology.get_domain_xml(
            "vm1"
        )
        self.assertEqual(result, "<xml/>")
        mock_run.assert_called_once_with(
            "virsh dumpxml vm1"
        )

    # =========================
    # parse_cpu_cache_from_xml
    # =========================
    def test_parse_cpu_cache_from_xml_success(self):
        xml = """
        <domain>
          <cpu>
            <model>Intel Xeon</model>

            <topology sockets="1" cores="2" threads="2"/>

            <cache level="1"
                   size="32"
                   unit="KiB"
                   type="data"
                   associativity="8"/>

            <cache level="2"
                   size="256"
                   unit="KiB"
                   type="unified"
                   associativity="4"/>

            <numa>
              <cell id="0"
                    cpus="0-3"
                    memory="4096"
                    unit="MiB"/>
            </numa>

          </cpu>
        </domain>
        """
        result = (
            get_vm_cpu_cache_topology
            .parse_cpu_cache_from_xml(xml)
        )
        self.assertEqual(
            result["cpu_model"],
            "Intel Xeon"
        )
        self.assertEqual(
            result["topology"]["cores"],
            2
        )
        self.assertIn(
            "L1",
            result["cache"]
        )
        self.assertIn(
            "0",
            result["numa"]
        )

    def test_parse_cpu_cache_from_xml_invalid(self):
        xml = "<domain><cpu>"
        result = (
            get_vm_cpu_cache_topology
            .parse_cpu_cache_from_xml(xml)
        )
        self.assertEqual(
            result["cpu_model"],
            ""
        )
        self.assertEqual(
            result["cache"],
            {}
        )

    # =========================
    # get_vm_cpu_cache_topology
    # =========================
    @patch(
        "gather.get_vm_cpu_cache_topology.time.time"
    )
    @patch(
        "gather.get_vm_cpu_cache_topology.parse_cpu_cache_from_xml"
    )
    @patch(
        "gather.get_vm_cpu_cache_topology.get_domain_xml"
    )
    def test_get_vm_cpu_cache_topology_success(
        self,
        mock_get_xml,
        mock_parse,
        mock_time
    ):
        mock_get_xml.return_value = "<xml/>"
        mock_parse.return_value = {
            "cpu_model": "Intel"
        }
        mock_time.return_value = 123456
        result = (
            get_vm_cpu_cache_topology
            .get_vm_cpu_cache_topology("vm1")
        )
        self.assertEqual(
            result["vm_name"],
            "vm1"
        )
        self.assertEqual(
            result["timestamp"],
            123456
        )

    @patch(
        "gather.get_vm_cpu_cache_topology.get_domain_xml"
    )
    def test_get_vm_cpu_cache_topology_no_xml(
        self,
        mock_get_xml
    ):
        mock_get_xml.return_value = None
        result = (
            get_vm_cpu_cache_topology
            .get_vm_cpu_cache_topology("vm1")
        )
        self.assertEqual(
            result,
            {}
        )

if __name__ == "__main__":
    unittest.main()
