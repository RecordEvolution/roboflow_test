from asyncio import sleep, get_event_loop, ensure_future
from reswarm import Reswarm
from roboflow import Roboflow
import cv2
import numpy as np
import base64
from datetime import datetime, timezone

rf = Roboflow(api_key="gi0b7TPcFZLVyeKO5Q42")
project = rf.workspace().project("hard-hat-sample-wa2pe")
local_inference_server_address = "http://localhost:9001/"

model = project.version(version_number=2, local=local_inference_server_address).model

camera = cv2.VideoCapture(0)

prediction_buffer = []

async def predictLoop():
    while True:
        _, img = camera.read()

        # Resize to improve speed
        height, width, channels = img.shape
        dim = min(height, width)
        img = cv2.resize(img, (dim, dim))

        # Send image to Roboflow Predict
        prediction = model.predict(img, confidence=40, overlap=30).json()
        now = datetime.now(timezone.utc)
        # Print prediction results
        payload = prediction['predictions']
        for pred in payload:
            del pred['image_path']
            pred['timestamp'] = now.isoformat()

        if len(payload) > 0:
            print(payload)
        else:
            print('nothing detected')
        prediction_buffer.extend(payload)
        await sleep(1)

async def publishLoop():
    rw = Reswarm()

    # Publishes data every 2 seconds to the 're.hello.world' topic
    while True:
        await sleep(2)
        # if len(prediction_buffer) == 0: continue
        data = prediction_buffer.copy()
        prediction_buffer.clear()
        await rw.publish('re.hello.world', data)

        print(f'Published {data} to topic re.hello.world')


async def main():
    ensure_future(predictLoop())
    await ensure_future(publishLoop())

if __name__ == "__main__":
    get_event_loop().run_until_complete(main())
