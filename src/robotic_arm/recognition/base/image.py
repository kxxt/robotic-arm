from robotic_arm.output import utter_async
from robotic_arm.recognition.base.base import RecognitionServiceBase


class ImageRecognitionService(RecognitionServiceBase):
    def __init__(self, name, output_queue_size=0):
        RecognitionServiceBase.__init__(self, name, output_queue_size)

    def real_work(self):
        try:
            self.output_queue.put(self.recognize(self.input_queue.get(block=True, timeout=5)))
        except:
            self.logger.warning("No input from input_queue!")

    def recognize(self, img):
        pass

    def recognize_sync(self):
        pass

    def wait_for_ready(self):
        if not self.loaded.isSet():
            self.logger.warning("Service is not ready when required! Probably performance issues.")
            utter_async("程序正在加载中,请稍后")
            self.loaded.wait()
