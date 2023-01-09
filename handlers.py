import cv2
import base64
from VideoCapture import VideoCapture

def take_picture(camera_connection):
    capture = cv2.VideoCapture(camera_connection.conn)
    ret, frame = capture.read()
    if ret is not True:
        raise Exception("could not read from camera")
    capture.release()
    ret, buffer = cv2.imencode(".jpg", frame)
    if ret is not True:
        raise Exception("could not encode image to jpg")
    return base64.b64encode(buffer)
