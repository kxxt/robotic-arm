from robotic_arm.recognition.base import ImageRecognitionService
import logging


class HandsRecognitionService(ImageRecognitionService):
    def __init__(self):
        ImageRecognitionService.__init__(self, 'hands-recognition')
        self.logger = logging.getLogger(__name__)

    def load(self):
        from time import sleep
        sleep(5)

    def recognize(self, img):
        pass
