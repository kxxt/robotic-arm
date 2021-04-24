from robotic_arm.config import FACE_RECOGNITION_SOLUTION,LOAD_REAL_SERVICES


if FACE_RECOGNITION_SOLUTION == "face_recognition":
    from robotic_arm.recognition.face_face_recognition_impl import FaceRecognitionService
elif FACE_RECOGNITION_SOLUTION == "mediapipe":
    from robotic_arm.recognition.face_mediapipe_impl import FaceRecognitionService
else:
    # Fake service! Not working.
    from robotic_arm.recognition.base.image import ImageRecognitionService as FaceRecognitionService

if LOAD_REAL_SERVICES:
    from robotic_arm.recognition.hands import HandsRecognitionService
    from robotic_arm.recognition.voice import VoiceRecognitionService
else:
    from robotic_arm.recognition.base.image import ImageRecognitionService as HandsRecognitionService
    from robotic_arm.recognition.base.image import ImageRecognitionService as VoiceRecognitionService
