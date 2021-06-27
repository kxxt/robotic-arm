import logging
logger = logging.getLogger("voice-composition-base")

class VoiceCompositionBase:
    _instance = []

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        logger.warning(f"Setting instance of VoiceCompositionBase to {instance}")
        cls._instance.append(instance)
        return instance

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @classmethod
    def get_instance(cls):
        logger.info(f"Retrieving Instance of VoiceCompositionBase: {cls._instance}")
        return cls._instance[-1]

    def utter(self, text: str):
        pass

    def utter_async(self, text: str):
        pass

    def utter_async_passive(self, text: str):
        pass

    def clear_async_queue(self):
        self.logger.warning("Doesn't support clearing async queue. Do nothing!")

    def wait_for_idle(self):
        self.logger.warning("Waiting for idle is not supported!")
