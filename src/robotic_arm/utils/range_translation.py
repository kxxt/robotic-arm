from numpy import interp

from robotic_arm.config import UNIFIED_RANGE


def translate(value, r, target=None):
    """translate to  UNIFIED_RANGE by default"""
    target = target or UNIFIED_RANGE
    return interp(value, r, target)


def inverse_translate(value, target, r=None):
    r = r or UNIFIED_RANGE
    return interp(value, r, target)
