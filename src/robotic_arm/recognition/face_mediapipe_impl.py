from robotic_arm.recognition.base import ImageRecognitionService
import logging
import numpy as np
from robotic_arm.input.camera import get_frame, get_raw_frame, wait_until_video_ready
from robotic_arm.config import MEDIAPIPE_FACE_DETECTION_MIN_CONFIDENCE
import mediapipe as mp
from datetime import datetime

mp_face_detection = mp.solutions.face_detection


class FaceRecognitionService(ImageRecognitionService):
    def __init__(self):
        ImageRecognitionService.__init__(self, 'face-recognition')
        self.logger = logging.getLogger('face-recognition-mpface')
        self.service = None
        self.process_this_frame = True

    def load(self):
        self.service = mp_face_detection.FaceDetection(min_detection_confidence=MEDIAPIPE_FACE_DETECTION_MIN_CONFIDENCE)
        wait_until_video_ready()
    # Raw detection format:
    # detections: iterable [
    #    @index [i]: PyObject {
    #       label_id: [int;1],
    #       score: [float;1],
    #       location_data: PyObject {
    #           format: int(enum), // usually 2
    #           relative_bounding_box: PyObject {
    #               xmin,ymin,width,height: float
    #           },
    #           relative_keypoints: PyObject {
    #               x,y: float
    #           }
    #       }
    #    }
    # ]
    def recognize(self, frame):
        if frame is None:
            return
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        frame.flags.writeable = False
        results = self.service.process(frame)

        # Draw the face detection annotations on the image.
        frame.flags.writeable = True
        return results

    def real_work(self):
        result = self.recognize(get_raw_frame())
        if result is not None and result.detections is not None:
            self.output_queue.put(result.detections)

    def recognize_sync(self):
        result = self.recognize(get_raw_frame())
        if result is not None and result.detections is not None:
            return result.detections
        return None
