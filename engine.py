from asyncio import sleep, get_event_loop, ensure_future, create_task
from reswarm import Reswarm
from roboflow import Roboflow
import cv2
import numpy as np
from datetime import datetime, timezone
import os
from aiohttp_jinja2 import setup, render_template_async
import jinja2

from aiohttp import web

rf = Roboflow(api_key=os.environ['ROBOFLOW_API_KEY'])
project = rf.workspace().project(os.environ['PROJECT'])
local_inference_server_address = "http://localhost:9001/"

model = project.version(version_number=os.environ.get('MODEL_VERSION', None), local=local_inference_server_address).model


def create_connection_from_env():
    rtsp_user = os.getenv("RTSP_USERNAME", "")
    rtsp_pwd = os.getenv("RTSP_PASSWORD", "")
    rtsp_ip = os.getenv("RTSP_IP", "")

    if rtsp_user != "" and rtsp_pwd != "" and rtsp_ip != "":
        print("Using env variables 'RTSP_IP', 'RTSP_USERNAME' & 'RTSP_PASSWORD' for RTSP Stream")
        rtsp_conn = f"rtsp://{rtsp_user}:{rtsp_pwd}@{rtsp_ip}/1"
        print(f"rtsp://{rtsp_user}:*****@{rtsp_ip}/1")
        return rtsp_conn
    else:
        print("Using USB Camera")
        camera_idx = int(os.getenv("USB_CAMERA_IDX", 0))
        return camera_idx


camera = cv2.VideoCapture(create_connection_from_env())

prediction_buffer = []
latest_image = None

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
            
        global latest_image
        latest_image = img
        # Resize to improve speed
        # height, width, channels = img.shape
        # dim = min(height, width)
        # img = cv2.resize(img, (dim, dim))
        # Send image to Roboflow Predict
        print('predict...')
        prediction = model.predict(img, confidence=os.environ['CONFIDENCE_THRESHOLD'], overlap=os.environ['OVERLAP_THRESHOLD']).json()
        now = datetime.now(timezone.utc)
        # Print prediction results
        predictions = prediction['predictions']
        for box in predictions:
            # example box result: [{'x': 234.3, 'y': 32.1, 'width': 44, 'height': 61, 'class': 'head', 'confidence': 0.557, 'prediction_type': 'ObjectDetectionModel'}]
            start = (int(box['x']) - int(box['width']/2), int(box['y']) - int(box['height']/2))
            end = (int(box['x']) + int(box['width']/2), int(box['y']) + int(box['height']/2))
            cv2.rectangle(img, start, end, (0, 255, 0), 2)
            # latest_image = np.copy(box['image_path'])
            del box['image_path']


        if len(predictions) > 0:
            # print(predictions)
            result = { "predictions": predictions, "timestamp": now.isoformat() }
            prediction_buffer.append(result)
        # else:
        #     print('nothing detected')

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
        sample = data[0]
        print(f'Published to topic ' + os.environ.get('PUBLISH_TOPIC') + f' {sample}')

async def init_app(app):
    app['publishLoop'] = create_task(publishLoop())
    app['predictLoop'] = create_task(predictLoop())


# async def serve_video(request):
#     return web.FileResponse('/app/output.mp4', headers={'content-type': 'video/mp4'})

async def serve_image(request):
    global latest_image
    if latest_image is None:
        return web.Response(text='no image received from camera', content_type='text/plain')
    ret, buffer = cv2.imencode(".jpg", latest_image)
    return web.Response(body=buffer.tobytes(), content_type="image/jpeg")

async def index(request):
    return await render_template_async('index.html', request, {
        "project": os.environ.get('PROJECT', 'no PROJECT specified'),
        "model_version": os.environ.get('MODEL_VERSION', 'no MODEL_VERSION specified'),
        "publish_to": os.environ.get('PUBLISH_TOPIC', 'no PUBLISH_TOPIC specified'),
        })
    # return web.FileResponse('/app/frontend/index.html')

if __name__ == "__main__":
    
    web_app = web.Application()
    setup(web_app, enable_async=True, loader=jinja2.FileSystemLoader('/app/frontend'))

    # web_app.router.add_get('/video', serve_video)
    web_app.router.add_get('/image', serve_image)
    web_app.router.add_get('/', index)
    web_app.on_startup.append(init_app)
    web.run_app(web_app, host='0.0.0.0', port=80)
    