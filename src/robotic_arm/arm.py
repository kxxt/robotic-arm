from transitions import Machine
from time import sleep
from robotic_arm.recognition import FaceRecognitionService, VoiceRecognitionService, HandsRecognitionService
import logging
from robotic_arm.output.voice import utter
from queue import Empty


class RoboticArm(Machine):
    states = ['welcoming', 'voice_detecting', 'face_detecting', 'hand_tracking']

    def __init__(self,
                 face_service: FaceRecognitionService,
                 voice_service: VoiceRecognitionService,
                 hands_service: HandsRecognitionService):
        Machine.__init__(
            self,
            states=RoboticArm.states,
            initial='welcoming')
        self.add_transition('welcomed', 'welcoming', 'voice_detecting')
        self.add_transition('voice_detected', 'voice_detecting', 'face_detecting')
        self.add_transition('pointed_at_face', 'face_detecting', 'hand_tracking')
        self.add_transition('max_time_reached', 'hand_tracking', 'voice_detecting')

        self.face_service = face_service
        self.voice_service = voice_service
        self.hands_service = hands_service

        self.logger = logging.getLogger(__name__)

    # BEGIN Voice command handlers

    # Handler Signature should be f: self -> shouldExitCommandLoop: bool

    def voice_command_hello_handler(self) -> bool:
        self.logger.info("Hello! From handler!")
        return False

    def voice_command_exit_handler(self) -> bool:
        self.logger.info("Exit! From handler!")
        return True

    def hash_negative_812530379159490365_handler(self) -> bool:
        self.logger.info(f"我十分同意你的观点!")
        utter("我十分同意你的观点!")
        return False

    # routes
    voice_command_handlers = {
        "Hello": voice_command_hello_handler,
        "Exit": voice_command_exit_handler,
        "-812530379159490365": hash_negative_812530379159490365_handler
    }

    def execute_voice_command(self, cmd: str) -> bool:
        self.logger.info(f"Executing voice command : {cmd}.")
        return self.voice_command_handlers[cmd](self)

    # END Voice command handlers

    # BEGIN Behavior definitions

    def perform_welcoming(self):
        print("Welcoming!")
        sleep(5)

    def perform_goodbye(self):
        print("Welcoming!")
        sleep(5)

    def on_enter_voice_detecting(self):
        print("Voice detecting!")
        self.voice_service.wait_for_ready()
        self.voice_service.start_working()
        while True:
            try:
                cmd = self.voice_service.output_queue.get(block=True, timeout=5)
                if self.execute_voice_command(cmd):
                    break
            except Empty:
                self.acquire_user_to_speak()

        self.voice_service.stop_working()

    def on_enter_face_detecting(self):
        print("face detecting")
        sleep(5)

    def on_enter_hand_tracking(self):
        print("Hand Tracking!")
        sleep(5)

    def acquire_user_to_speak(self):
        utter("你他妈的说话啊!")

    # END Behavior definitions

    def run(self):
        self.perform_welcoming()
        self.welcomed()
        # 当识别到"退出程序"时 , voice_detected 失败, 返回False 结束循环
        while self.voice_detected():
            self.pointed_at_face()
            self.max_time_reached()
            pass
        self.perform_goodbye()
