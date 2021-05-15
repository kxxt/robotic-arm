import roboticstoolbox as rtb
from roboticstoolbox.backends.swift import Swift
from robotic_arm.motion.base import MotionBase


class SimulatedMotion(MotionBase):
    def __init__(self):
        self.robot = None
        self.backend = None

    def load(self):
        self.robot = rtb.models.Panda()
        self.backend = Swift()
        self.backend.launch()
        self.backend.add(self.robot)

    def set(self, servo_id, value):
        self.robot.q[servo_id] = value
        self.backend.step()

    def set_all(self, value):
        self.robot.q = value
        self.backend.step()
