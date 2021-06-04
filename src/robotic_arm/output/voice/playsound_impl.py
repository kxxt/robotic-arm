import logging
from playsound import playsound
from robotic_arm.output.voice.static_voice_preprocessor import get
from robotic_arm.output.voice.base import VoiceCompositionBase


class PlaysoundVoiceComposition(VoiceCompositionBase):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("playsound")

    def utter(self, text: str):
        self.logger.debug(f"Playing sound {get(text)}")
        playsound(get(text), block=True)

    def utter_async(self, text: str):
        playsound(get(text), block=False)

    def utter_async_passive(self, text: str):
        self.logger.warning("Doesn't support passive async uttering! Text will be uttered async.")
        self.utter_async(text)
