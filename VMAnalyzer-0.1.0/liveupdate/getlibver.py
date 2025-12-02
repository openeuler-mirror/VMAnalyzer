#!/usr/bin/python
#
# Get disk serial info from a domain
#

import libvirt
import sys
from lxml import etree


SERVER_NAME = "qemu+ssh://root@192.168.203.132/system"
LOCAL_NAME = "qemu:///system"
def createConnection(serverName):
  if not libvirt:
    print 'python-libvirt module is missing'
    sys.exit(1)
#  conn = libvirt.openReadOnly("qemu+ssh://root@192.168.203.132/system")
  conn = libvirt.openReadOnly(serverName)
  if conn == None:
    print 'Failed to connect to QEMU/KVM'
  else:
    print '------------Connected to QEMU/KVM---------------'
    return conn
  
def closeConnection(conn):
  try:
    print '----------Disconnect from QEMU/KVM--------------'
    conn.close()
  except:
    print 'Failed to close connection'
    sys.exit(1)

def getESSDSerial(domain, conn):
  if domain == None:
    print 'Domain Name Is Empty'
    sys.exit(1)
  dom = conn.lookupByName(domain)
  tree = etree.fromstring(dom.XMLDesc(0))
  for disk_info in tree.findall('devices/disk'):
    device = disk_info.find('target').get('dev')
    if device and (device.startswith('sd') or device.startswith('vd')):
      serial = disk_info.find('serial')
      volume_uuid = serial.text if serial is not None else None
      print 'disk: %s / serial : %s ' % (device, volume_uuid)

if __name__ == '__main__':
  argc = len(sys.argv) - 1
  print(argc)
  if argc == 0:
      libvirtServer = "qemu:///system"
  else:
      libvirtServer = "qemu+ssh://root@" + sys.argv[1] + "/system"
  conn = createConnection(libvirtServer)
  #getESSDSerial(domainName, conn)
  pack = conn.getLibPackage()
  ver = conn.getLibVersion()
  print("libvirt version : {}\nlibvert package info : {}".format(ver, pack))

  closeConnection(conn)
  


