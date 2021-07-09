import threading
from robotic_arm.config import LIGHT_PIN
from robotic_arm.gpio import pi, pigpio
from time import sleep


class Light:
    def __init__(self, pin: int = None):
        self.pin = pin or LIGHT_PIN
        self.thread = threading.Thread(target=self.working, daemon=True)
        self.flicker = threading.Event()
        pi.set_mode(self.pin, pigpio.OUTPUT)

    def start_flicker(self):
        self.flicker.set()

    def stop_flicker(self):
        self.flicker.clear()

    def working(self):
        while True:
            self.flicker.wait()
            while self.flicker.is_set():
                self.on()
                sleep(0.5)
                self.off()

    def switch(self, state: bool):
        pi.write(self.pin, state)

    def on(self):
        pi.write(self.pin, 1)

    def off(self):
        pi.write(self.pin, 0)
