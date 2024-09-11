#!/bin/bash
ip link set dev wlx9cefd5f986da name wlan0
ip link set wlan0 down
iw wlan0 set type mp
ip link set wlan0 up
iw wlan0 mesh join wiseMesh freq 2422
ip addr add 192.168.1.3/24 dev wlan0

