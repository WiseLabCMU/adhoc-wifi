#!/bin/bash
# Usage: sudo ./iwup.sh 3
# - Parameter $1 is the named IP subnet address number to use, unique for this device.
# - "wlx*"" is a wild card for the default NIC interface name (e.g. wlx9cefd5f986da), change if needed.
# - "wlan0" is only a convenience shorthand for CLI tests, change if needed.
# - "wiseMesh" is a name for a network pool, change if needed.
# - "2422" is the frequency of the wi-fi channel to use, change if needed.

if [ $# -eq 0 ]
  then
    echo "No arguments supplied, add last ip subnet."
    exit 1
fi
ip_part=$1

# remove desktop network manager
sudo systemctl stop network-manager.service
#sudo systemctl disable network-manager.service

# testing query for wireless interface
interface="wlan0"
if /sbin/ethtool wlan0 | grep -q "No such device"; then
#if ip link show wlan0 | grep -q "does not exist"; then
 interface=$(find /sys/class/net/ -name "wlx*" -exec basename \{} \;)
 echo "$interface renamed to wlan0"
 sudo ip link set dev $interface name wlan0
fi
# sudo ip link set dev wlx9cefd5f986da name wlan0

sudo ip link set wlan0 down
sudo iw wlan0 set type mp
sudo ip link set wlan0 up
sudo iw wlan0 mesh join wiseMesh freq 2422
sudo ip addr add 192.168.1.$ip_part/24 dev wlan0
