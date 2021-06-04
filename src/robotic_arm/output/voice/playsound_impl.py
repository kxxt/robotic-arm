import logging
from playsound import playsound
from robotic_arm.output.voice.static_voice_preprocessor import get

logger = logging.getLogger("playsound")


def utter(text: str):
    logger.debug(f"Playing sound {get(text)}")
    playsound(get(text), block=True)


def utter_async(text: str):
    playsound(get(text), block=False)


def utter_async_passive(text: str):
    logger.warning("Doesn't support passive async uttering! Text will be uttered async.")
    utter_async(text)


def clear_async_queue():
    logger.warning("Doesn't support clearing async queue. Do nothing!")
