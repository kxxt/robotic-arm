from robotic_arm.config import DIGITAL_SERVO_PIN
from robotic_arm.motion.base import ServoBase

from robotic_arm.gpio import pi


class DigitalServo(ServoBase):
    def __init__(self, pin=None):
        self.pin = pin or DIGITAL_SERVO_PIN

    def load(self):
        pi.set_PWM_range(self.pin, 20000)  # 5是要输出PWM的IO口， 20000设定PWM的调节范围，
        # 我们的舵机的控制信号是50Hz，就是20ms为一个周期。就是20000us。
        # 设为20000,就是最小调节为1us
        pi.set_PWM_frequency(self.pin, 50)  # 设定PWM的频率，5是要设定的IO口， 50 是频率

    def set(self, value, time=1000):
        # 0,1000 -> 0,180
        pi.set_PWM_frequency(self.pin, value)

    def get(self):
        return pi.get_PWM_dutycycle(self.pin)
