class MotionBase:
    def load(self):
        pass

    def set(self, servo_id, value):
        pass

    def set_all(self, value):
        pass


class ServoBase:
    def load(self):
        pass

    def set(self, value):
        pass

    def exec(self, cmd, param):
        pass
