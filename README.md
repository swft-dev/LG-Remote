# LG WebOS TV Web Remote

A web remote for LG Smart TVs running webOS. Hosted locally on your home network via Flask, allowing you to control your TV from any phone, tablet, or browser without needing external apps.

Includes built-in **Wake-on-LAN (WoL)** magic packets to turn the TV on even when it is in standby.

---

## Features

- **Responsive Touch Remote:** Clean, dark-mode interface built for phones and desktop browsers.
- **Full Navigation:** D-pad directional arrows, OK/Enter, Back, and Home buttons.
- **Media Controls:** Volume up/down, mute toggle, play/pause.
- **Power Control:** Standby power off via WebOS API + power on via Wake-on-LAN magic packets.
- **Haptic Feedback:** Native mobile vibration support on button taps.

---

## Requirements

1. **Python 3.8+** installed on your host machine.
2. **TV Network Settings:**
   - Both your host PC and LG TV must be connected to the **same local network** (Wi-Fi or Ethernet).
   - On your TV, navigate to **Settings > General > Devices > External Devices > Turn on via Wi-Fi / Mobile** (Wake-on-LAN) and enable it.
   - **Recommended:** Open your home router settings (usually `192.168.1.1` or `192.168.0.1`) and assign a **DHCP Static IP Reservation** to your LG TV so its IP address never changes.

---

## Installation

1. Clone or download this repository to your computer.
2. Open your terminal or command prompt inside the project folder.
3. Install the required Python packages:

```bash
pip install flask pywebostv
