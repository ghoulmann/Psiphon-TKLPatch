#!/usr/bin/python
#
#By Rik Goldman
#On boot, choose an proxy available only to the lan for administration
import sys
import time
import getopt
import socket
import fcntl
import struct
import ipaddr
import netifaces
import MySQLdb
#from IPy import IP

#from http://code.activestate.com/recipes/439094
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifname[:15])
    )[20:24])

hostnames=[]
available=netifaces.interfaces()
#print available
#print "Add ip addresses of available interfaces"
for ifname in available:
    try:
        hostnames.append(get_ip_address(ifname))
#        print hostnames
    except IOError:
#        print 'ifname not available'
        available.remove(ifname)
#print hostnames

for ip in hostnames:
    if ipaddr.IPv4Address(ip)!="IPv4Address":
        hostnames.remove(ip)

#print "remove addresses that are not IPv4Addresses"
for ip in hostnames:
    if not ip.startswith("192.168") or ip.startswith("10.") or ip.startswith("172."):
        hostnames.remove(ip)
#print hostnames
#print "remaining hostnames"
#print hostnames

hostname=hostnames[0]

#print hostname

for ifs in available:
    try:
        match = get_ip_address(ifs)
        if match == hostname:
            interface = ifs
    except IOError:
        available.remove(ifs)

#print "HOSTNAME"
#print hostname
#print "Interface"
#print interface

#Read defaults, update psiphon.proxy so the proxy called administrative has the ip determined by the script
db=MySQLdb.connect(read_default_file="/etc/mysql/debian.cnf")
proxy="""UPDATE psiphon.proxy SET hostname = \"%s\" WHERE name="administrative";""" % (hostname)

db.query(proxy)
