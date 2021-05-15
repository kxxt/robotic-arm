from robotic_arm.recognition.base import ImageRecognitionService
import logging
import numpy as np
from robotic_arm.input.camera import get_frame
from datetime import datetime


class FaceRecognitionService(ImageRecognitionService):
    def __init__(self):
        ImageRecognitionService.__init__(self, 'face-recognition')
        self.logger = logging.getLogger('face-recognition-facerec')
        self.service = None
        self.process_this_frame = True

    def load(self):
        self.service = __import__("face_recognition")

    known_face_encodings = []
    known_face_names = []

    def recognize(self, frame):
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = self.service.face_locations(frame)
            face_encodings = self.service.face_encodings(frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = self.service.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = self.service.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

                face_names.append(name)
            self.process_this_frame = not self.process_this_frame
            return face_names, face_locations, face_encodings
        self.process_this_frame = not self.process_this_frame

    def real_work(self):
        result = self.recognize(get_frame())
        if result is not None:
            self.output_queue.put(result)
