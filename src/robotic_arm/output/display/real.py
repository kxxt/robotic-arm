from robotic_arm.config import OLED_DISPLAY_DRIVER, OLED_DISPLAY_INTERFACE, OLED_DISPLAY_WIDTH, OLED_DISPLAY_HEIGHT
from robotic_arm.output.display.device import get_device


def init_device_from_config():
    return get_device([
        f"--display={OLED_DISPLAY_DRIVER}",
        f"--interface={OLED_DISPLAY_INTERFACE}",
        f"--width={OLED_DISPLAY_WIDTH}",
        f"--height={OLED_DISPLAY_HEIGHT}"
    ])
