#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

def validate_interval(interval: int) -> bool:
    """Check if the collection interval is valid."""
    return isinstance(interval, int) and interval > 0

def validate_timeout(timeout: int) -> bool:
    """Check if the timeout value is valid."""
    return isinstance(timeout, int) and timeout > 0

def validate_vm_id(vm_id: int) -> bool:
    """Check if the VM ID is valid."""
    return isinstance(vm_id, int) and vm_id >= 0
