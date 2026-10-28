# Make sure wake on LAN is enabled. Check with your TV model if it's available
# If wake on LAN is not available on your TV, skip this part

import socket

TV_IP = ""
MAC = ""
BROADCAST = ""

clean_mac = MAC.replace(":", "").replace("-", "")
mac_bytes = bytes.fromhex(clean_mac)
packet = b'\xff' * 6 + mac_bytes * 16

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print("Blasting Wake-on-LAN packets...")
for port in [9, 7]:
    sock.sendto(packet, (BROADCAST, port))
    sock.sendto(packet, (TV_IP, port))
sock.close()

print("Check if the TV turned on.")
