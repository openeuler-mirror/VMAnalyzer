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
VM_DOMAIN_EVENT_DEFINED = "defined"
VM_DOMAIN_EVENT_UNDEFINED = "undefined"
VM_DOMAIN_EVENT_STARTED = "started"
VM_DOMAIN_EVENT_SUSPENDED = "suspended"
VM_DOMAIN_EVENT_RESUMED = "resumed"
VM_DOMAIN_EVENT_STOPPED = "stopped"
VM_DOMAIN_EVENT_SHUTDOWN = "shutdown"
VM_DOMAIN_EVENT_PMSUSPENDED = "PMSuspended"
VM_DOMAIN_EVENT_CRASHED = "crashed"

VM_DOMAIN_SUPPORTED_EVENTS = (VM_DOMAIN_EVENT_DEFINED,
                              VM_DOMAIN_EVENT_UNDEFINED,
                              VM_DOMAIN_EVENT_STARTED,
                              VM_DOMAIN_EVENT_SUSPENDED,
                              VM_DOMAIN_EVENT_RESUMED,
                              VM_DOMAIN_EVENT_STOPPED,
                              VM_DOMAIN_EVENT_SHUTDOWN,
                              VM_DOMAIN_EVENT_PMSUSPENDED,
                              VM_DOMAIN_EVENT_CRASHED)

VM_DOMAIN_EVENT_CALLBACK = {
    VM_DOMAIN_EVENT_CRASHED : 'add_vm'
}

CONNECTION_CLOSE_REASON_ERROR = "ERROR"
CONNECTION_CLOSE_REASON_EOF = "End-Of-File"
CONNECTION_CLOSE_REASON_KEEPALIVE = "Keepalive"
CONNECTION_CLOSE_REASON_CLIENT = "Client"

CONNECTION_CLOSE_REASON_STRINGS = (CONNECTION_CLOSE_REASON_ERROR,
                                   CONNECTION_CLOSE_REASON_EOF,
                                   CONNECTION_CLOSE_REASON_KEEPALIVE,
                                   CONNECTION_CLOSE_REASON_CLIENT)
