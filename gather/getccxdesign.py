#!/usr/bin/python
# _*_coding: utf-8 _*_

import libvirt
import sys


LOCAL_NAME = "qemu:///system"
def createConnection(serverName):
    if not serverName:
        print("错误：serverName 不能为空")
        sys.exit(1)

    if not libvirt:
        print("错误：未找到libvirt库")
        sys.exit(1)

    conn = libvirt.openReadOnly(serverName)
    if conn is None:
        print('Failed to connect to QEMU/KVM')
    else:
        return conn

def closeConnection(conn):
    try:
        if conn:
            conn.close()
    except:
        sys.exit(1)

if __name__ == '__main__':

    conn = createConnection(LOCAL_NAME)
    try:
        ccx = conn.virHostGetCCXDesign()
        print("ccx design:")
        print(ccx)
    except libvirt.libvirtError as e:
        print(f'获取CCX Design失败：{e}')

    closeConnection(conn)
