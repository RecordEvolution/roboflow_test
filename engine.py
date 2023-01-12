from asyncio import sleep, get_event_loop, ensure_future, create_task
from reswarm import Reswarm
from roboflow import Roboflow
import cv2
import numpy as np
import base64
from datetime import datetime, timezone
import os

from aiohttp import web

rf = Roboflow(api_key="gi0b7TPcFZLVyeKO5Q42")
project = rf.workspace().project("hard-hat-sample-wa2pe")
local_inference_server_address = "http://localhost:9001/"

model = project.version(version_number=2, local=local_inference_server_address).model

camera = cv2.VideoCapture(0)
print(camera)

prediction_buffer = []

async def predictLoop():
    print('starting predict loop')
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # out = cv2.VideoWriter('/app/output.mp4', fourcc, float(20), (640, 480))

    while True:
        await sleep(1/20)
        ret, img = camera.read()
        if not ret: 
            print('no image read from camera')
            continue
            
        # Resize to improve speed
        height, width, channels = img.shape
        dim = min(height, width)
        img = cv2.resize(img, (dim, dim))
        # Send image to Roboflow Predict
        prediction = model.predict(img, confidence=40, overlap=30).json()

        now = datetime.now(timezone.utc)
        # Print prediction results
        predictions = prediction['predictions']
        for box in predictions:
            # cv2.rectangle(img, (box['x'], box['y']), (box['x'] + box['width'], box['y'] + box['height']), (0, 255, 0), 2)
            del box['image_path']

        if len(predictions) > 0:
            print(predictions)
            result = { "predictions": predictions, "timestamp": now.isoformat() }
            prediction_buffer.append(result)
            # [{'x': 234.3, 'y': 32.1, 'width': 44, 'height': 61, 'class': 'head', 'confidence': 0.557, 'prediction_type': 'ObjectDetectionModel'}]
        else:
            print('nothing detected')

        # out.write(img)
        # sz = os.path.getsize('/app/output.mp4')
        # print(sz)


async def publishLoop():
    print('starting publish loop')

    rw = Reswarm()

    # Publishes data every 2 seconds to the 're.roboflow.data' topic
    while True:
        await sleep(2)
        if len(prediction_buffer) == 0: continue
        data = prediction_buffer.copy()
        prediction_buffer.clear()
        await rw.publish(os.environ.get('PUBLISH_TOPIC'), data)

        print(f'Published {data} to topic ' + os.environ.get('PUBLISH_TOPIC'))

async def init_app(app):
    app['publishLoop'] = create_task(publishLoop())
    app['predictLoop'] = create_task(predictLoop())


async def serve_video(request):
    return web.FileResponse('/app/output.mp4', headers={'content-type': 'video/mp4'})

async def index(request):
    return web.FileResponse('/app/index.html')

if __name__ == "__main__":
    
    web_app = web.Application()
    web_app.router.add_get('/video', serve_video)
    web_app.router.add_get('/', index)
    web_app.on_startup.append(init_app)
    web.run_app(web_app, host='0.0.0.0', port=80)
    