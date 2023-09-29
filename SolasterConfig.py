import json

data = {
  "channel_defaults": {},
  "server": {
    "serverIP": "10.10.101.1",
    "debug": True,
    "http_debug": False,
    "http_demo": True,
    "http_dir": "web",
    "http_login": "demo",
    "http_password": "demo",
    "http_port": ":8083",
    "https": False,
    "https_auto_tls": False,
    "https_auto_tls_name": "",
    "https_cert": "server.crt",
    "https_key": "server.key",
    "https_port": ":443",
    "ice_credential": "",
    "ice_servers": [
      "stun:stun.l.google.com:19302"
    ],
    "ice_username": "",
    "log_level": "debug",
    "rtsp_port": ":5541",
    "token": {
      "backend": "http://127.0.0.1/test.php",
      "enable": False
    },
    "webrtc_port_max": 0,
    "webrtc_port_min": 0
  },
  "streams": {
    "Front Camera": {
      "channels": {
        "0": {
          "deviceNumber": "Solaster",
          "audio": True,
          "url": "rtsp://10.10.1.1:8554/stream"
        }
      },
      "name": "Front Camera"
    },
    "Bottom Camera": {
      "channels": {
        "0": {
          "deviceNumber": "Solaster",
          "url": "rtsp://10.10.1.1:8555/zed-stream"
        }
      },
      "name": "Bottom Camera"
    }
  }
}

with open('RTSPtoWeb/config.json', 'w') as f:
    json.dump(data, f, indent=4)