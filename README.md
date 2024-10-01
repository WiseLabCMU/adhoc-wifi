# Testing configuration of low-power wifi adhoc networks on Jetson Orin Nano.

## Configuration Attempts

### 1. First Steps:

- Tried with Jetson SDK Desktop at first: https://developer.nvidia.com/embedded/jetpack-sdk-60
- Disabled network manager service to avoid fighting configurations.
- Result: Onboard Realtek wifi hardware/drivers report **adhoc (ibss)** available, but commands failed silently.

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
- Result: Onboard Realtek wifi hardware/drivers report **adhoc (ibss)** available, but commands failed silently.

### 3. New NIC Hardware Try:

- Some links for linux-friendly adapters, including second link of 802.11s mesh point compatible ones:
  - https://github.com/morrownr/USB-WiFi/blob/main/home/USB_WiFi_Adapters_that_are_supported_with_Linux_in-kernel_drivers.md#n150---usb-2---24-ghz-wifi-4
  - https://github.com/phillymesh/802.11s-adapters
- Added Panda wifi USB adapter: https://www.amazon.com/Panda-Ultra-150Mbps-Wireless-Adapter/dp/B00762YNMG
- Result: USB Panda wifi hardware/drivers report **adhoc (ibss) and mesh** available, both sets of commands worked.

### 4. Add GUI Components

- `sudo apt install slim ubuntu-desktop`
- ...

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
  - Naturally cell division will occur and nodes `A,B` will still be able to communicate with each other, as will `C,D`.
- When either `A,B` and `C,D` come back within range of each other, the network will re-merge and be restored for full routing from/to each node once again
  ```
  B ---------- A ------------- C ---------- D
  ```
  - **Note:** In simple wireless adhoc mode, this remerge after fragmentation is _unreliable_, and In fact even on initial network initialization can result in cell division despite what should be viable physical wireless links.

## Next Steps

- Add ROS 2 node
- Add ROS Viz2
- ROS to UDP bridge without retries or fragmentation
