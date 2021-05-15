from multiprocessing import Process, Queue

from robotic_arm.motion.base import MotionBase
from robotic_arm.motion.simulation import SimulatedMotion


def event_loop(q: Queue, target_cls):
    motion = target_cls()
    motion.load()
    while msg := q.get(block=True):
        if len(msg) != 2:
            motion.set_all(msg)
        else:
            motion.set(msg[0], msg[1])


class MultiprocessingSimulatedMotion(MotionBase):
    def __init__(self):
        self.proc = None
        self.queue = Queue()

    def load(self):
        self.proc = Process(target=event_loop, args=(self.queue, SimulatedMotion), daemon=True)
        self.proc.start()

    def set(self, s, v):
        self.queue.put((s, v))

    def set_all(self, value):
        self.queue.put(value)
