import cv2
from robotic_arm.config import CAMERA_ID

video_capture = cv2.VideoCapture(CAMERA_ID)


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
