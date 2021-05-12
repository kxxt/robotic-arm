from robotic_arm.config import SERVO_IMPLEMENTATION

if SERVO_IMPLEMENTATION == 'simulated':
    from robotic_arm.motion.simulation import SimulatedMotion as Motion
elif SERVO_IMPLEMENTATION == 'real':
    from robotic_arm.motion.reality import RealMotion as Motion
else:
    from robotic_arm.motion.base import MotionBase as Motion
