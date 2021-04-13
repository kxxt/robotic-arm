from robotic_arm.output.voice import load
load()

from robotic_arm import RoboticArm
import logging
from robotic_arm.recognition import *

logger = logging.getLogger(__name__)

face_service = FaceRecognitionService()
hands_service = HandsRecognitionService()
voice_service = VoiceRecognitionService()
face_service.run()
hands_service.run()
voice_service.run()

arm = RoboticArm(face_service, voice_service, hands_service)
arm.run()
