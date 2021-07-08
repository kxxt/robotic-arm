from robotic_arm.motion.base import MotionBase
from robotic_arm.config import SERVO_SERIAL_PATH, SERVO_SERIAL_BAUD
from robotic_arm.motion.reality.serial import lib
from robotic_arm.utils.range_translation import translate, inverse_translate

from functools import partial


class SerialServos(MotionBase):
    def __init__(self, ids=None, ran=None):
        super().__init__()
        self.ids = ids
        self.handle = lib.acquire_serial_handle()
        self._write = partial(lib.servo_exec,
                              handle=self.handle,
                              cmd=lib.servo_commands["write"])
        self._read = partial(lib.servo_read,
                             handle=self.handle)
        self.range = ran or (0, 1000)

    def load(self):
        lib.init_servo_board()

    def set(self, id, value, time=1000):
        value = inverse_translate(value, self.range)
        self._write(id=id, par1=value, par2=time)

    def set_all(self, value, time=1000):
        raise NotImplementedError()

    def get(self, id):
        return translate(self._read(id=id), self.range)

    def get_all(self):
        if self.ids is None:
            raise ValueError("Please set ids of the SerialServos first!")
        return [self.get(id) for id in self.ids]
