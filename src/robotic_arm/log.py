from robotic_arm.config import LOGGING_LEVEL

def init_logger():
    import logging

    logger = logging.getLogger()
    logger.setLevel(level=LOGGING_LEVEL)
    file_handler = logging.FileHandler("robotic-arm.log")
    file_handler.setLevel(LOGGING_LEVEL)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOGGING_LEVEL)
    file_handler.setFormatter(logging.Formatter('%(asctime)s [%(name)s]@%(threadName)s|%(levelname)s: %(message)s'))
    console_handler.setFormatter(logging.Formatter('%(asctime)s [%(name)s]@%(threadName)s|%(levelname)s: %(message)s'))
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
