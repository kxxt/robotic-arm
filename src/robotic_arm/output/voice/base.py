import logging


class VoiceCompositionBase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        cls._instance = instance
        return instance

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @classmethod
    def get_instance(cls):
        return cls._instance

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
