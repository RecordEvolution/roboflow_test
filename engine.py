from asyncio.events import get_event_loop
from asyncio import sleep
from reswarm import Reswarm
from roboflow import Roboflow
import cv2
import numpy as np
import base64

rf = Roboflow(api_key="gi0b7TPcFZLVyeKO5Q42")
project = rf.workspace().project("hard-hat-sample-wa2pe")
local_inference_server_address = "http://localhost:9001/"

model = project.version(version_number=2, local=local_inference_server_address).model

camera = cv2.VideoCapture(0)

while True:
    _, img = camera.read()

    # Resize to improve speed
    height, width, channels = img.shape
    dim = min(height, width)
    img = cv2.resize(img, (dim, dim))

    # Send image to Roboflow Predict
    prediction = model.predict(img, confidence=40, overlap=30).json()

    # Print prediction results
    payload = prediction['predictions']
    for pred in payload:
        del pred['image_path']

    if len(payload) > 0:
        print(payload)

# async def main():
#     rw = Reswarm()

#     # Publishes sample data every 2 seconds to the 're.hello.world' topic
#     while True:
#         data = {"temperature": 20}
#         await rw.publish('re.hello.world', data)

#         print(f'Published {data} to topic re.hello.world')

#         await sleep(2)



# if __name__ == "__main__":
#     get_event_loop().run_until_complete(main())