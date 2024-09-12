# Testing configuration of low-power wifi adhoc networks on Jetson Orin Nano.

## Test scripts, testing mesh mode. 
- `sudo apt install iw wireless-tools`
- `sudo ./iwup.sh`
- `python3 ping.py`

## Configuration Attempts

### 1. First Steps: 
- Tried with Jetson SDK Desktop at first: https://developer.nvidia.com/embedded/jetpack-sdk-60
- Disabled network manager service to avoid fighting configurations.
- Result: Onboard Realtek wifi hardware/drivers report **adhoc (ibss)** available, but commands failed silently.

### 2. Eliminating OS/Drivers Setup:
- Update BIOS
- Flash ubuntu server 22 for Jetso Orin Nano: https://ubuntu.com/download/nvidia-jetson
- sudo apt dist-upgrade
- `sudo reboot`
- https://pages.ubuntu.com/rs/066-EOV-335/images/Ubuntu_22.04_for_NVIDIA_Jetson_Orin_Instructions.pdf
- sudo apt install nvidia-tegra drivers per doc above “Install NVIDIA proprietary software”
- Result: Onboard Realtek wifi hardware/drivers report **adhoc (ibss)** available, but commands failed silently.

### 3. New NIC Hardware Try:
- Some links for linux-friendly adapters, including second link of 802.11s mesh point compatible ones:
    - https://github.com/morrownr/USB-WiFi/blob/main/home/USB_WiFi_Adapters_that_are_supported_with_Linux_in-kernel_drivers.md#n150---usb-2---24-ghz-wifi-4
    - https://github.com/phillymesh/802.11s-adapters
- Added Panda wifi USB adapter: https://www.amazon.com/Panda-Ultra-150Mbps-Wireless-Adapter/dp/B00762YNMG
- Result: USB Panda wifi hardware/drivers report **adhoc (ibss) and mesh** available, both sets of commands worked.
