import logging
import os
from robotic_arm.output import load_display_service
from robotic_arm.output import load_voice_composition_service

disp = load_display_service()
load_voice_composition_service()

from robotic_arm import RoboticArm
from robotic_arm.recognition import *
from robotic_arm.motion import Motion

logger = logging.getLogger(__name__)

motion = Motion()

# WORK-AROUND FOR SIMULATION
# 因为模拟在运行时会把当前目录切到磁盘根目录
# 影响其他服务的加载
# 所以这里有一个 UGLY WORK-AROUND

work_dir = os.getcwd()
motion.load()
os.chdir(work_dir)

face_service = FaceRecognitionService()
hands_service = HandsRecognitionService()
voice_service = VoiceRecognitionService()
face_service.run()
hands_service.run()
voice_service.run()

arm = RoboticArm(face_service, voice_service, hands_service, motion, disp)
arm.run()
