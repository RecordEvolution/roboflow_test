# from asyncio.events import get_event_loop
# from asyncio import sleep
from reswarm import Reswarm
from roboflow import Roboflow

rf = Roboflow(api_key="gi0b7TPcFZLVyeKO5Q42")
project = rf.workspace().project("hard-hat-sample-wa2pe")
local_inference_server_address = "http://localhost:9001/"

model = project.version(version_number=2, local=local_inference_server_address).model

while True:
    # Capture image from camera
    camera = cv2.VideoCapture(0)
    _, image = camera.read()

    # Send image to Roboflow Predict
    prediction = model.predict(image, confidence=40, overlap=30).json()

    # Print prediction results
    print(prediction)

    # infer on a local image
    # print(model.predict("your_image.jpg", confidence=40, overlap=30).json())

    # visualize your prediction
    # model.predict("your_image.jpg", confidence=40, overlap=30).save("prediction.jpg")

    # infer on an image hosted elsewhere
    # print(model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json())

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