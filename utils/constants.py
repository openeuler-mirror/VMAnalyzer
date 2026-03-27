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

# Libvirt domain event type IDs (VIR_DOMAIN_EVENT_* from libvirt.h).
# These are integer values passed by libvirt to domain-event callbacks.
# The order must match the libvirt enumeration exactly so that
# VM_DOMAIN_SUPPORTED_EVENTS[event_id] returns the human-readable name.
VM_DOMAIN_EVENT_DEFINED    = 0
VM_DOMAIN_EVENT_UNDEFINED  = 1
VM_DOMAIN_EVENT_STARTED    = 2
VM_DOMAIN_EVENT_SUSPENDED  = 3
VM_DOMAIN_EVENT_RESUMED    = 4
VM_DOMAIN_EVENT_STOPPED    = 5
VM_DOMAIN_EVENT_SHUTDOWN   = 6
VM_DOMAIN_EVENT_PMSUSPENDED = 7
VM_DOMAIN_EVENT_CRASHED    = 8

# Human-readable names indexed by event integer ID.
VM_DOMAIN_SUPPORTED_EVENTS = (
    "defined",       # 0
    "undefined",     # 1
    "started",       # 2
    "suspended",     # 3
    "resumed",       # 4
    "stopped",       # 5
    "shutdown",      # 6
    "PMSuspended",   # 7
    "crashed",       # 8
)

# Libvirt connection-close reason IDs (VIR_CONNECT_CLOSE_REASON_* from libvirt.h).
CONNECTION_CLOSE_REASON_ERROR     = 0
CONNECTION_CLOSE_REASON_EOF       = 1
CONNECTION_CLOSE_REASON_KEEPALIVE = 2
CONNECTION_CLOSE_REASON_CLIENT    = 3

CONNECTION_CLOSE_REASON_STRINGS = (
    "ERROR",       # 0
    "End-Of-File", # 1
    "Keepalive",   # 2
    "Client",      # 3
)
