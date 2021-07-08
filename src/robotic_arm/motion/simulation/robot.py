import roboticstoolbox as rtb

try:
    from roboticstoolbox.backends.swift import Swift
except:
    from roboticstoolbox.backends.Swift import Swift

from robotic_arm.motion.base import MotionBase
from robotic_arm.motion.physics import PhysicalModel


class SimulatedMotion(MotionBase):
    def __init__(self):
        self.robot = None
        self.backend = None

    def load(self):
        self.robot = PhysicalModel()
        self.backend = Swift()
        self.backend.launch()
        self.backend.add(self.robot)

    def for_test_purpose(self):
        import spatialmath as sm
        import numpy as np
        Tep = self.robot.fkine(self.robot.q) * sm.SE3.Tx(0.2) * sm.SE3.Ty(0.2) * sm.SE3.Tz(0.45)
        arrived = False
        while not arrived:
            # Work out the required end-effector velocity to go towards the goal
            v, arrived = rtb.p_servo(self.robot.fkine(self.robot.q), Tep, 1)
            # Set the self.robot's joint velocities
            self.robot.qd = np.linalg.pinv(self.robot.jacobe(self.robot.q)) @ v
            # Step the simulator by 50 milliseconds
            self.backend.step(0.05)

    def set(self, servo_id, value, time=50):
        self.robot.q[servo_id] = value
        self.backend.step(time / 1000)

    def set_all(self, value, time=50):
        self.robot.q = value
        self.backend.step(50 / 1000)
