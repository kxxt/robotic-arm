from robotic_arm.config import DIGITAL_SERVO_PIN
from robotic_arm.motion.base import ServoBase
from robotic_arm.utils.range_translation import translate, inverse_translate
from robotic_arm.gpio import pi


class DigitalServo(ServoBase):
    def __init__(self, pin=None, ran=None):
        super().__init__()
        self.pin = pin or DIGITAL_SERVO_PIN
        self.range = ran or (500, 2500)

    def load(self):
        pi.set_PWM_range(self.pin, 20000)  # 5是要输出PWM的IO口， 20000设定PWM的调节范围，
        # 我们的舵机的控制信号是50Hz，就是20ms为一个周期。就是20000us。
        # 设为20000,就是最小调节为1us
        pi.set_PWM_frequency(self.pin, 50)  # 设定PWM的频率，5是要设定的IO口， 50 是频率

    def set(self, value, time=1000):
        pi.set_PWM_frequency(self.pin, inverse_translate(value, self.range))

    def get(self):
        return translate(pi.get_PWM_dutycycle(self.pin), self.range)
