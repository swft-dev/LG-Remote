# This is to pair your PC to your TV
# Because IP addresses change a lot, please make a reservation IP at router settings (e.g. http://192.168.0.1/)

import json
from pywebostv.connection import WebOSClient

TV_IP = "" # TV's IP address

print(f"Connecting to TV {TV_IP}")
client = WebOSClient(TV_IP)
client.connect()

store = {}
print("Click 'ACCEPT' on TV")

for status in client.register(store):
    if status == WebOSClient.PROMPTED:
        print("Prompt displayed on TV screen")
    elif status == WebOSClient.REGISTERED:
        print("Pairing complete.")

with open("tv_key.json", "w") as f:
    json.dump(store, f)

print("Key saved to tv_key.json")
