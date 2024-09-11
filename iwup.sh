#!/bin/bash

# testing query for wireless interface
#interface="wlan0"
#if /sbin/ethtool wlan0 | grep -q "No such device"; then
##if ip link show wlan0 | grep -q "does not exist"; then
#  interface=$(find /sys/class/net/ -name "wlx*" -exec basename \{} \;)
#  echo "$interface renamed to wlan0"
#  ip link set dev $interface name wlan0
#fi

ip link set dev wlx9cefd5f986da name wlan0
ip link set wlan0 down
iw wlan0 set type mp
ip link set wlan0 up
iw wlan0 mesh join wiseMesh freq 2422
ip addr add 192.168.1.3/24 dev wlan0

