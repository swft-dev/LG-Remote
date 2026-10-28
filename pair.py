import json
from pywebostv.connection import WebOSClient

TV_IP = ""

print(f"Connecting to LG TV at {TV_IP}...")
client = WebOSClient(TV_IP)
client.connect()

store = {}
print("LOOK AT YOUR TV SCREEN NOW AND CLICK 'ACCEPT'...")

for status in client.register(store):
    if status == WebOSClient.PROMPTED:
        print("Prompt displayed on TV screen...")
    elif status == WebOSClient.REGISTERED:
        print("SUCCESS! Pairing complete.")

with open("tv_key.json", "w") as f:
    json.dump(store, f)

print("Key saved to tv_key.json. You will never need to pair again.")
