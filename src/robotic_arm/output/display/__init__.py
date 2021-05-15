from robotic_arm.config import OLED_DISPLAY_IMPLEMENTATION

if OLED_DISPLAY_IMPLEMENTATION == 'real':
    from robotic_arm.output.display.real import init_device_from_config
elif OLED_DISPLAY_IMPLEMENTATION == 'simulated':
    from robotic_arm.output.display.simulated import init_device_from_config
else:
    def init_device_from_config(args):
        pass


def load_display_service():
    from robotic_arm.output.display.display import Display
    d = Display(init_device_from_config())
    d.start()
    return d
