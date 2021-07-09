from robotic_arm.input.sensors.base import SensorBase
from robotic_arm.gpio import pi, pigpio
from robotic_arm.config import LIGHTNESS_SENSOR_PIN


class LightSensor(SensorBase):
    def __init__(self, pin=None):
        self.pin = pin or LIGHTNESS_SENSOR_PIN
        pi.set_mode(self.pin, pigpio.INPUT)

    def read(self):
        return pi.read(self.pin)
