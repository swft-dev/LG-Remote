import json
import os
import socket
from flask import Flask, render_template_string, jsonify, request
from pywebostv.connection import WebOSClient
from pywebostv.controls import MediaControl, SystemControl, InputControl

app = Flask(__name__)

TV_IP = ""
TV_MAC = ""
BROADCAST_IP = ""
PORT = 5500
KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tv_key.json")

client = None
media = None
system = None
inp = None

def wake_tv():
    clean_mac = TV_MAC.replace(":", "").replace("-", "")
    mac_bytes = bytes.fromhex(clean_mac)
    packet = b'\xff' * 6 + mac_bytes * 16

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    for port in [9, 7]:
        sock.sendto(packet, (BROADCAST_IP, port))
        sock.sendto(packet, (TV_IP, port))
    sock.close()

def get_tv():
    global client, media, system, inp
    if client is not None:
        try:
            system.info()
            return True
        except Exception:
            client = None

    if not os.path.exists(KEY_FILE):
        return False

    try:
        with open(KEY_FILE, "r") as f:
            store = json.load(f)

        new_client = WebOSClient(TV_IP)
        new_client.connect()
        for _ in new_client.register(store):
            pass

        client = new_client
        media = MediaControl(client)
        system = SystemControl(client)
        inp = InputControl(client)
        inp.connect_input()
        return True
    except Exception:
        client = None
        return False

HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>LG Remote</title>
  <style>
    * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
    body {
      background: #0f1015;
      color: #fff;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      margin: 0;
      user-select: none;
    }
    .remote {
      display: flex;
      flex-direction: column;
      gap: 14px;
      width: 280px;
    }
    .row {
      display: flex;
      gap: 10px;
    }
    button {
      background: #1c1d24;
      color: #fff;
      border: 1px solid #2d2e38;
      border-radius: 14px;
      padding: 16px;
      font-size: 15px;
      font-weight: 700;
      cursor: pointer;
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 6px rgba(0,0,0,0.3);
      transition: all 0.08s ease;
    }
    button:active {
      background: #2563eb;
      transform: scale(0.95);
    }
    .btn-power-on { 
      background: #15803d; 
      border-color: #166534; 
    }
    .btn-power-on:active { 
      background: #16a34a; 
    }
    .btn-power-off { 
      background: #5f1414; 
      border-color: #7f1d1d; 
    }
    .btn-power-off:active { 
      background: #dc2626; 
    }
    .dpad {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-gap: 10px;
      margin: 8px 0;
    }
    .dpad button { height: 60px; font-size: 18px; }
  </style>
</head>
<body>
  <div class="remote">
    <div class="row">
      <button class="btn-power-on" onclick="send('power_on')">ON</button>
      <button class="btn-power-off" onclick="send('power_off')">OFF</button>
      <button onclick="send('home')">HOME</button>
    </div>

    <div class="dpad">
      <div></div>
      <button onclick="send('up')">▲</button>
      <div></div>
      <button onclick="send('left')">◀</button>
      <button onclick="send('ok')">OK</button>
      <button onclick="send('right')">▶</button>
      <div></div>
      <button onclick="send('down')">▼</button>
      <div></div>
    </div>

    <div class="row">
      <button onclick="send('vol_down')">VOL -</button>
      <button onclick="send('mute')">MUTE</button>
      <button onclick="send('vol_up')">VOL +</button>
    </div>

    <div class="row">
      <button onclick="send('back')">BACK</button>
      <button onclick="send('play')">PLAY / PAUSE</button>
    </div>
  </div>

  <script>
    function send(act) {
      if (navigator.vibrate) navigator.vibrate(35);
      fetch('/api/cmd', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: act })
      });
    }
  </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_UI)

@app.route('/api/cmd', methods=['POST'])
def cmd():
    global client
    action = request.json.get('action')

    if action == 'power_on':
        wake_tv()
        return jsonify(status="ok")

    if not get_tv():
        return jsonify(status="error", error="TV starting up or unreachable"), 503

    try:
        if action == 'vol_up': media.volume_up()
        elif action == 'vol_down': media.volume_down()
        elif action == 'mute': media.mute(True)
        elif action == 'up': inp.up()
        elif action == 'down': inp.down()
        elif action == 'left': inp.left()
        elif action == 'right': inp.right()
        elif action == 'ok': inp.ok()
        elif action == 'back': inp.back()
        elif action == 'home': inp.home()
        elif action == 'play': media.play()
        elif action == 'power_off':
            system.power_off()
            client = None
        return jsonify(status="ok")
    except Exception as e:
        client = None
        return jsonify(status="error", error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
