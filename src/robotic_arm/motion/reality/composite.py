from robotic_arm.motion.base import MotionBase
from robotic_arm.motion.reality.serial import SerialServos
from robotic_arm.motion.reality.digital import DigitalServo


class CompositeMotion(MotionBase):
    def __init__(self, dig: DigitalServo, ser: SerialServos):
        self.digital_servo = dig
        self.serial_servos = ser

    def set(self, id, value, time=1000):
        if id == 1:
            self.digital_servo.set(value, time)
        else:
            self.serial_servos.set(id - 1, value, time)

    def set_all(self, values, time=1000):
        self.digital_servo.set(values[0], time)
        self.serial_servos.set(values[1:], time)

    def get(self, id):
        if id == 1:
            return self.digital_servo.get()
        else:
            return self.serial_servos.get(id - 1)

    def get_all(self):
        return [self.digital_servo.get(), *self.serial_servos.get_all()]
