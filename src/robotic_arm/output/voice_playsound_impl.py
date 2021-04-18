import logging
from playsound import playsound
from robotic_arm.output.static_voice_preprocessor import load, get

logger = logging.getLogger("playsound")


def utter(text: str):
    logger.debug(f"Playing sound {get(text)}")
    playsound(get(text), block=True)


def utter_async(text: str):
    playsound(get(text), block=False)
