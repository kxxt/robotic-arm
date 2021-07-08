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

    def camera_to_world(self, cpos, dis=1):
        """

        :param cpos: numpy ndarray , camera position.
        :return: world position
        """
        return (self.links[5].A(self.q[4]) @ self.links[4].A(self.q[3]) @ self.links[3].A(self.q[2])
                @ self.links[2].A(self.q[1]) @ self.links[1].A(self.q[0])).inv() @ np.append(cpos, [dis, 1])
