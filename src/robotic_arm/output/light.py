from colour import Color
import pigpio

from robotic_arm.config import LIGHT_PIN
from robotic_arm.gpio import pi


class Light:
    def __init__(self, pin: int = None):
        self.pin = pin or LIGHT_PIN
        pi.set_mode(self.pin, pigpio.OUTPUT)

    def switch(self, state: bool):
        pi.write(self.pin, state)

    def on(self):
        pi.write(self.pin, 1)

    def off(self):
        pi.write(self.pin, 1)
