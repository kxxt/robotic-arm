from multiprocessing import Process, Queue

from robotic_arm.motion.base import MotionBase
from robotic_arm.motion.simulation import SimulatedMotion


def event_loop(q: Queue, target_cls):
    motion = target_cls()
    motion.load()
    while msg := q.get(block=True):
        if callable(msg):
            msg(motion)
        elif len(msg) != 2:
            motion.set_all(msg)
        else:
            motion.set(msg[0], msg[1])


def for_test_purpose(self: SimulatedMotion):
    import spatialmath as sm
    import roboticstoolbox as rtb
    import numpy as np
    self.robot.q = self.robot.qr
    Tep = self.robot.fkine(self.robot.q) * sm.SE3.Tx(0.2) * sm.SE3.Ty(0.2) * sm.SE3.Tz(0.45)
    arrived = False
    while not arrived:
        # Work out the required end-effector velocity to go towards the goal
        v, arrived = rtb.p_servo(self.robot.fkine(self.robot.q), Tep, 1)
        # Set the self.motion.robot's joint velocities
        self.robot.qd = np.linalg.pinv(self.robot.jacobe(self.robot.q)) @ v
        # Step the simulator by 50 milliseconds
        self.backend.step(0.05)


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

    def for_test_purpose(self):
        self.send_function(for_test_purpose)

    def send_function(self, func):
        self.queue.put(func)
