from robotic_arm.recognition.base import ImageRecognitionService
import logging


class FaceRecognitionService(ImageRecognitionService):
    def __init__(self):
        ImageRecognitionService.__init__(self, 'face-recognition')
        self.logger = logging.getLogger(__name__)

    def load(self):
        from time import sleep
        sleep(5)

    def recognize(self, img):
        pass
