import logging
import os
from robotic_arm.input import init_video_device_async
from robotic_arm.output import load_display_service, utter_async
from robotic_arm.output import load_voice_composition_service
from robotic_arm.output.voice import register_voice_output_callback
from robotic_arm.config import NAME

logger = logging.getLogger(__name__)
logger.info("Loading display service ...")

disp = load_display_service()
register_voice_output_callback(lambda x: disp.println(x))
load_voice_composition_service()
utter_async(f"欢迎使用智能机械臂，我叫{NAME}，程序还在加载，请稍等片刻")

init_video_device_async()

from robotic_arm import RoboticArm
from robotic_arm.recognition import *
from robotic_arm.motion import Motion

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
