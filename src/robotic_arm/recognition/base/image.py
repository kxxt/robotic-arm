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
