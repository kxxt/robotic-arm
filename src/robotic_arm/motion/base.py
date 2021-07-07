class MotionBase:
    def load(self):
        pass

    def set(self, servo_id, value, time=1000):
        pass

    def set_all(self, value, time=1000):
        pass

    def get(self, servo_id):
        pass

    def get_all(self):
        pass


class ServoBase:
    def load(self):
        pass

    def set(self, value, time=1000):
        pass

    def get(self):
        pass

    def exec(self, cmd, param):
        pass
