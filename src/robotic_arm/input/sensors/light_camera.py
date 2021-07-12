from robotic_arm.input.sensors.base import SensorBase
from robotic_arm.input.camera import get_frame
import numpy as np
import cv2


class LightSensor(SensorBase):
    def __init__(self):
        pass

    def read(self):
        frame = get_frame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean = np.mean(gray)
        print(mean)
        return mean > 50
