from robotic_arm.recognition.base import ImageRecognitionService
from robotic_arm.config import HANDS_MIN_DETECTION_CONFIDENCE, HANDS_MIN_TRACKING_CONFIDENCE
from robotic_arm.input.camera import get_frame, get_raw_frame
import mediapipe as mp
import logging

mp_hands = mp.solutions.hands


class HandsRecognitionService(ImageRecognitionService):
    def __init__(self):
        ImageRecognitionService.__init__(self, 'hands-recognition', 5)
        self.logger = logging.getLogger('hands-recognition')
        self.service = None
        self.process = 0

    def load(self):
        self.service = mp_hands.Hands(
            min_detection_confidence=HANDS_MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=HANDS_MIN_TRACKING_CONFIDENCE)

    def recognize(self, frame):
        self.process += 1
        if frame is None or self.process % 3 == 1:
            return
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        frame.flags.writeable = False
        results = self.service.process(frame)

        # Draw the face detection annotations on the image.
        frame.flags.writeable = True
        return results

    # Data format:
    # multi_hand_landmarks: iter = [
    #     hand_landmarks = {
    #         landmark:iter = {
    #             {
    #                 x,y,z
    #             },...
    #         }
    #     },...
    # ]
    def real_work(self):
        result = self.recognize(get_raw_frame())
        if result is not None and result.multi_hand_landmarks is not None:
            if self.output_queue.full():
                self.output_queue.get()
            self.output_queue.put(result.multi_hand_landmarks)

    def recognize_sync(self):
        result = self.recognize(get_raw_frame())
        if result is not None and result.multi_hand_landmarks is not None:
            return result.multi_hand_landmarks
