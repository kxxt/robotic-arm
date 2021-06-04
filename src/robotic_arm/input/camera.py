from typing import Union

import cv2
from cv2.cv2 import VideoCapture

from robotic_arm.config import CAMERA_ID
import threading

video_capture: Union[VideoCapture, None] = None
video_ready: threading.Event = threading.Event()


def is_video_ready():
    return video_ready.is_set()


def init_video_device():
    global video_capture, video_ready
    cv2.VideoCapture(CAMERA_ID)
    video_ready.set()


def init_video_device_async():
    global video_capture
    thread = threading.Thread(target=init_video_device, name="init-video", daemon=True)
    thread.start()


def get_raw_frame():
    """
    Get raw camera frame (RGB)
    :return: Raw frame from camera (RGB)
    """
    success, image = video_capture.read()
    if not success:
        return None
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # convert to RGB from BGR


def get_frame(fx=0.25, fy=0.25):
    """
    Return resized frame (a quarter by default)
    :param fx: x resize factor
    :param fy: y resize factor
    :return: resized frame
    """
    success, image = video_capture.read()
    if not success:
        return None
    return cv2.cvtColor(cv2.resize(image, (0, 0), fx, fy), cv2.COLOR_BGR2RGB)
