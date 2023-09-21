import json

data = {
  "channel_defaults": {},
  "server": {
    "serverIP": "192.168.3.12",
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
    "demo": {
      "channels": {
        "0": {
          "deviceNumber": 1,
          "audio": True,
          "url": "rtsp://220.254.72.200/Src/MediaInput/h264/stream_1"
        }
      },
      "name": "111111111"
    },
    "demo1": {
      "channels": {
        "0": {
          "deviceNumber": 1,
          "url": "rtsp://admin:12345@95.154.86.198:554/"
        }
      },
      "name": "dsadsa"
    },
    "demo2": {   
      "channels": {
        "0": {
          "deviceNumber": 1,
          "url": "rtsp://admin:12345@95.154.86.198:554/"
        }
      },
      "name": "ad"
    }
  }
}

with open('RTSPtoWeb/config.json', 'w') as f:
    json.dump(data, f, indent=4)