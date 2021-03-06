from typing import Union

import cv2

try:
    from cv2 import VideoCapture
except:
    from cv2.cv2 import VideoCapture

from robotic_arm.config import CAMERA_ID
from robotic_arm.output import VoiceCompositionBase

import logging
import threading

import numpy as np

video_capture: Union[VideoCapture, None] = None
video_ready: threading.Event = threading.Event()

logger = logging.getLogger("camera")


def is_video_ready():
    return video_ready.is_set()


def wait_until_video_ready():
    if is_video_ready():
        return
    VoiceCompositionBase.get_instance().utter("正在等待摄像头设备启动，请稍候。")
    video_ready.wait()


def init_video_device():
    global video_capture, video_ready
    video_capture = cv2.VideoCapture(CAMERA_ID)
    video_ready.set()


def init_video_device_async():
    global video_capture
    thread = threading.Thread(target=init_video_device, name="init-video", daemon=True)
    thread.start()


def get_raw_frame():
    wait_until_video_ready()
    while True:
        try:
            success, image = video_capture.read()
            break
        except:
            logger.warning("Failed to read from video capture! Retrying...")
    return image if success else None


def get_unresized_frame():
    """
    Get raw camera frame (RGB)
    :return: Raw frame from camera (RGB)
    """
    wait_until_video_ready()
    while True:
        try:
            success, image = video_capture.read()
            break
        except:
            logger.warning("Failed to read from video capture! Retrying...")
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
    wait_until_video_ready()
    while True:
        try:
            success, image = video_capture.read()
            break
        except:
            logger.warning("Failed to read from video capture! Retrying...")
    if not success:
        return None
    return cv2.cvtColor(cv2.resize(image, (int(fx * np.size(image, 0)), int(fy * np.size(image, 1)))),
                        cv2.COLOR_BGR2RGB)
