# LG WebOS TV Web Remote

A remote for LG TVs that's hosted on your network, allowing you to control your TV from your browser.

## Requirements

1. **Python**
2. **TV Network Settings:**
   - Both your host PC and LG TV must be connected to the **same local network** (Wi-Fi or Ethernet).
   - On your TV, navigate to **Settings > General > Devices > External Devices > Turn on via Wi-Fi / Mobile** (Wake-on-LAN) and enable it.
   - **Recommended:** Open your home router settings (usually `192.168.1.1` or `192.168.0.1`) and assign a **DHCP Static IP Reservation** to your LG TV so its IP address never changes.

## Installation

1. Download this repository to your computer.
2. Open your terminal or command prompt inside the project folder.
3. Install the required Python packages:

```Bash
pip install flask pywebostv
```

### Note: To start the server, run app.py
