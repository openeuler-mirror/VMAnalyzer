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
import libvirt
from argparse import ArgumentParser

parser = ArgumentParser(description=__doc__)
parser.add_argument("domain")

args = parser.parse_args()

try:
    conn = libvirt.open(None)
except libvirt.libvirtError:
    print("failed to open")
    exit(1)

try:
    dom = conn.lookupByName(args.domain)
except libvirt.libvirtError:
    print(f"ERROR: domain '{args.domain}' is not running or does not exist")
    exit(0)

downtime = dom.liveupgrade(1, 2000, -1, None)
print(downtime)
