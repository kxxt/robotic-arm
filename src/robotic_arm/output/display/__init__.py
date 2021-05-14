from robotic_arm.config import OLED_DISPLAY_IMPLEMENTATION
from robotic_arm.output.display import real,simulated

oled = real.init_device_from_config() if OLED_DISPLAY_IMPLEMENTATION == 'real' else simulated.init_device_from_config()
