import requests
import base64
from websockets.sync.client import connect
import json


def test_deepgram():
    with open("/Users/jm/repos/tax-chatterbox/test/preamble.wav", "rb") as f:
        audio_content = f.read()
        encoded_audio = base64.b64encode(audio_content).decode("utf-8")

        with connect("ws://localhost:8001/ws/v1/audio") as ws:
            ws.send(json.dumps({"buffered": encoded_audio}))
            resp = ws.recv()
            print(json.loads(resp))


if __name__ == "__main__":
    test_deepgram()