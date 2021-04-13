import cv2
from robotic_arm.config import CAMERA_ID

video_capture = cv2.VideoCapture(CAMERA_ID)


def get_raw_frame():
    """
    Get raw camera frame (RGB)
    :return: Raw frame from camera (RGB)
    """
    return video_capture.read()[:, :, ::-1]  # convert to RGB from BGR


def get_frame(fx=0.25, fy=0.25):
    """
    Return resized frame (a quarter by default)
    :param fx: x resize factor
    :param fy: y resize factor
    :return: resized frame
    """
    return cv2.resize(video_capture.read(), (0, 0), fx, fy)[:, :, ::-1]
