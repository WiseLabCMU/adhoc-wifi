# Testing configuration of low-power wifi adhoc networks on Jetson Orin Nano.

## Configuration Attempts

### 1. First Steps:

- Tried with Jetson SDK Desktop at first: https://developer.nvidia.com/embedded/jetpack-sdk-60
- Disabled network manager service to avoid fighting configurations.
- Result: Onboard Realtek wifi hardware/drivers report adhoc (ibss) available, but **commands failed silently**.

### 2. Eliminating OS/Drivers Setup:

- Update BIOS
- Flash ubuntu server 22 for Jetso Orin Nano: https://ubuntu.com/download/nvidia-jetson
- Update general ubuntu packages
  ```
   sudo apt dist-upgrade
   sudo reboot
  ```
- Install nvidia-tegra drivers per doc [Install NVIDIA proprietary software](https://pages.ubuntu.com/rs/066-EOV-335/images/Ubuntu_22.04_for_NVIDIA_Jetson_Orin_Instructions.pdf)
  ```
  sudo add-apt-repository ppa:ubuntu-tegra/updates
  sudo apt install -y nvidia-tegra-drivers-36
  sudo usermod -a -G render,video ubuntu
  sudo reboot
  ```
  - **WARNING: When using Ubuntu Desktop 22 from Jetson SDK, installing the `nvidia-tegra` drivers inexplicably nukes all other drivers (display, network, etc) on the device.**
- Install ubuntu package `iw` to manage wireless config
  ```
  sudo apt install -y iw
  ```
- Result: Onboard Realtek wifi hardware/drivers report **adhoc (ibss)** available, but commands still failed silently.

### 3. New NIC Hardware Try:

- Some links for linux-friendly adapters, including second link of 802.11s mesh point compatible ones:
  - https://github.com/morrownr/USB-WiFi/blob/main/home/USB_WiFi_Adapters_that_are_supported_with_Linux_in-kernel_drivers.md#n150---usb-2---24-ghz-wifi-4
  - https://github.com/phillymesh/802.11s-adapters
- Added Panda wifi USB adapter: https://www.amazon.com/Panda-Ultra-150Mbps-Wireless-Adapter/dp/B00762YNMG
- Result: USB Panda wifi hardware/drivers report **adhoc (ibss) and mesh** available, both sets of commands worked.
- Added ALFA Network AWUS036ACM wifi USB adapter: https://www.amazon.com/dp/B08BJS8FXD
- Result: Wifi hardware/drivers (`mt76x2u`) report **adhoc (ibss) and mesh** available, both sets of commands worked.

### 4. Add GUI Components (optional)

- `sudo apt install slim ubuntu-desktop`

## Test scripts, testing mesh mode.

- `sudo apt install iw`
- `sudo ./iwup.sh`
- `python3 ping.py`

## Testing Mesh Network recovery

- Given nodes `A, B, C, D` arranged "linearly" by position and physical wireless links:
  ```
  A ---------- B ------------- C ---------- D
  ```
  802.11s will automatically route the entire network from/to each node
- When the network topology fragments, e.g.
  ```
  A ---------- B               C ---------- D
  ```
  - Naturally cell division will occur and nodes `A,B` will still be able to communicate with each other, as will `C,D`. Connection drops can be simulated by simply setting TX power to 0, which will limit viable connection range to a few feet.
- When either `A,B` and `C,D` come back within range of each other, the network will re-merge and be restored for full routing from/to each node once again. 
  ```
  B ---------- A ------------- C ---------- D
  ```
  - **Note:** In simple wireless adhoc mode, this remerge after fragmentation is _unreliable_, and in fact even first ad-hoc network initialization can result in cell division despite what should be viable physical wireless links.

# ROS2
Per https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html

```
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update && sudo apt upgrade -y
```
And either ROS default graphical bundle if using wiith Ubuntu Desktop, ROS2 and RViz will be installed
```
sudo apt install ros-humble-desktop
```

OR just `ros-base` for ROS2 CLI-only
```
sudo apt install ros-humble-ros-base
```

## MQTT2UDP (future ROS2UDP) Bridge
We create an example of using [UDP to bridge MQTT messages](udp_bridge.py) with conceptually similar publish/subscribe functionality.
While in this case there is a shared MQTT broker, a drop-in replacement with ROS2 would have each device subscribing
and publishing to its own respective local ROS instance.

## Next Steps
- Set ROS to loopback only (don't let it interact with mesh subnet)
- Setup Isaac ROS Dev Base containers
