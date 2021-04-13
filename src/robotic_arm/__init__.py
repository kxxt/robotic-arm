from robotic_arm.log import init_logger
import logging

init_logger()

logger = logging.getLogger(__name__)
logger.info("Initializing Robotic Arm")

from robotic_arm.arm import RoboticArm
