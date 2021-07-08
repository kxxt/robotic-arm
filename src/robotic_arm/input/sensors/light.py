from robotic_arm.input.sensors.base import SensorBase
from robotic_arm.gpio import pi
from robotic_arm.config import LIGHTNESS_SENSOR_PIN

import pigpio


class LightSensor(SensorBase):
    def __init__(self, pin=None):
        self.pin = pin or LIGHTNESS_SENSOR_PIN
        pi.set_mode(self.pin, pigpio.INPUT)

    def read(self):
        return pi.read(self.pin)
