import roboticstoolbox as rtb
import numpy as np
from roboticstoolbox.robot import ERobot
from roboticstoolbox import RevoluteDH, PrismaticDH
import spatialmath as sm
from math import pi
from robotic_arm.config import URDF_PATH


class PhysicalModel(ERobot):
    def __init__(self):
        links, name = self.URDF_read(URDF_PATH)
        super().__init__(
            links, name=name, manufacturer="Robot"
        )
