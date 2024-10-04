Commands installed/tested:
```bash
sudo apt update
sudo add-apt-repository ppa:ubuntu-tegra/updates
sudo apt dist-upgrade
sudo reboot now
lshw -c network
sudo apt install -y nvidia-tegra-drivers-37
sudo apt install -y nvidia-tegra-drivers-36
sudo usermod -a -G render,video ubuntu
sudo apt update
sudo apt dist-upgrade
sudo reboot now
wget https://raw.githubusercontent.com/WiseLabCMU/adhoc-wifi/refs/heads/main/iwup.sh
wget https://raw.githubusercontent.com/WiseLabCMU/adhoc-wifi/refs/heads/main/ping.py
lshw -C network
sudo lshw -C network
chmod +x iwup.sh
sudo ./iwup.sh 1
find /sys/class/net
ip a
sudo ip link set dev wlx9cefd5f9a33e wlan0
sudo ip link set dev wlx9cefd5f9a33e name wlan0
sudo ./iwup.sh 1
iw
sudo apt install -y iw
sudo ./iwup.sh 1
iw dev wlan0
iw dev wlan0 station dump
iw dev wlan0 mesh
iw dev wlan mpath dump
sudo iw dev wlan mpath dump
sudo iw dev wlan0 link
sudo iw dev wlan0 info
ip a
sudo iw dev wlan0 info
sudo iw dev wlan0 station dump
sudo iw dev wlan0 info
sudo iw dev wlan0 link
sudo iw dev wlan0 mpath dump
ping 192.168.1.3
ping 192.168.1.4
sudo iw dev wlan0 mpath dump
python3 ping.py 1
sudo iw dev wlan0 set txpower fixed 0
sudo iw dev wlan0 info
sudo iw dev wlan0 dump station
sudo iw dev wlan0 links
sudo iw dev wlan0 link
sudo iw dev wlan0
sudo iw
sudo iw dev wlan0 info
sudo iw dev wlan0 dump station
sudo iw dev wlan0 station dump
ping 192.168.1.2
ping 192.168.1.3
ping 192.168.1.4
sudo apt install slim
sudo apt install ubuntu-desktop
sudo service slim start
sudo service NetworkManager stop
sudo systemctl disable NetworkManager
sudo ./iwup.sh 1
ros run turtlesim turtle_teleop key
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtle_teleop_key
```
