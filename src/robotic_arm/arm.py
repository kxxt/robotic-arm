import logging
from queue import Empty
import os

import cv2
from transitions import Machine

from robotic_arm.config import NAME
from robotic_arm.input.camera import get_raw_frame
from robotic_arm.output import VoiceCompositionBase
from robotic_arm.recognition import FaceRecognitionService, VoiceRecognitionService, HandsRecognitionService
from robotic_arm.utils import get_center_point, is_point_at_camera_center
from robotic_arm.motion.base import MotionBase


class RoboticArm(Machine):
    states = ['welcoming', 'voice_detecting', 'face_detecting', 'hand_tracking']

    def __init__(self,
                 face_service: FaceRecognitionService,
                 voice_service: VoiceRecognitionService,
                 hands_service: HandsRecognitionService,
                 voice_composition: VoiceCompositionBase,
                 motion_impl: MotionBase,
                 display_service):
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
        self.voice_composition = voice_composition

        self.utter = voice_composition.utter
        self.utter_async = voice_composition.utter_async
        self.utter_async_passive = voice_composition.utter_async_passive

        self.motion = motion_impl
        self.display = display_service

        self.logger = logging.getLogger(__name__)

    # BEGIN Voice command handlers

    # Handler Signature should be f: self -> shouldExitCommandLoop: bool

    def voice_command_hello_handler(self) -> bool:
        self.logger.info("Hello! From handler!")
        self.utter_async("我好得很!")
        return False

    def voice_command_start_handler(self) -> bool:
        self.logger.info("Start! From handler!")
        self.utter_async(f"{NAME}来了")
        return True

    def voice_command_exit_handler(self) -> bool:
        self.logger.info("Exit! From handler!")
        self.perform_goodbye()
        return True

    def hash_negative_812530379159490365_handler(self) -> bool:
        self.logger.info(f"我十分同意你的观点!")
        self.utter("我十分同意你的观点!")
        return False

    def hash_7951174358884070940_handler(self) -> bool:
        self.utter("很多人都以为我疯啦!")
        return False

    # routes
    voice_command_handlers = {
        "Hello": voice_command_hello_handler,
        "Exit": voice_command_exit_handler,
        "Start": voice_command_start_handler,
        "-812530379159490365": hash_negative_812530379159490365_handler,
        "7951174358884070940": hash_7951174358884070940_handler
    }

    def execute_voice_command(self, cmd: str) -> bool:
        self.logger.info(f"Executing voice command : {cmd}.")
        return self.voice_command_handlers[cmd](self)

    # END Voice command handlers

    # BEGIN Behavior definitions

    def perform_welcoming(self):
        self.utter("程序加载完成，试试对我说小亮小亮。")

    def perform_goodbye(self):
        self.utter("感谢您的使用，程序即将退出。")
        self.display.device.cleanup()
        os._exit(0)

    def on_enter_voice_detecting(self):
        self.voice_service.wait_for_ready()
        self.voice_service.start_working()
        while True:
            try:
                cmd = self.voice_service.output_queue.get(block=True, timeout=10)
                if self.execute_voice_command(cmd):
                    break
            except Empty:
                self.acquire_user_to_speak()
                # self.motion.for_test_purpose(0.1, 0.2, 0.3)
        self.voice_service.stop_working()

    def on_enter_face_detecting(self):
        import mediapipe as mp
        drawing = mp.solutions.drawing_utils
        print("face detecting")
        self.face_service.wait_for_ready()
        # self.face_service.start_working()
        locked = False

        def act_on_no_body(found):
            if found:
                self.utter_async_passive("你去哪了,我正在找你呢?")
            else:
                self.utter_async_passive("人都去哪了？")

        while True:
            result = self.face_service.recognize_sync()
            if result is None:
                act_on_no_body(locked)
                continue
            image = None
            while image is None:
                image = get_raw_frame()
            for detection in result:
                drawing.draw_detection(image, detection)
            cv2.imshow("Face", image)
            le = len(result)
            if le == 0:
                act_on_no_body(locked)
            elif le == 1:
                if not locked:
                    self.utter_async("已经圈定一个人")
                    locked = True
                posx, posy = get_center_point(result[0].location_data)
                self.logger.debug(f"x:{posx},y:{posy}")
                if is_point_at_camera_center(posx, posy):
                    self.voice_composition.clear_async_queue()
                    self.voice_composition.wait_for_idle()
                    self.utter(f"{NAME}对准您了，可以用手势指挥我。")
                    break
                else:
                    self.utter_async_passive("正在将摄像头对准您")
            else:
                self.utter_async(f"已经在{le}个人中圈定了一个人")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # self.face_service.stop_working()

    def on_enter_hand_tracking(self):
        import mediapipe as mp
        mp_drawing = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands
        self.hands_service.wait_for_ready()
        self.hands_service.start_working()
        executed = False
        while True:
            frame = get_raw_frame()
            if frame is None:
                continue
            try:
                # marks = None
                # while not self.hands_service.output_queue.empty():
                #    marks = self.hands_service.output_queue.get_nowait()
                marks = self.hands_service.output_queue.get()
                if not marks:
                    self.logger.info("Encountered empty marks!")
                    continue
                for mark in marks:
                    mp_drawing.draw_landmarks(
                        frame, mark, mp_hands.HAND_CONNECTIONS)
                if not executed:
                    executed = True
                    mark = marks[0]
                    self.motion.for_test_purpose(mark.landmark[0].x, mark.landmark[0].y, 0.4)
                cv2.imshow("Hands", frame)
            except Empty:
                pass
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.hands_service.stop_working()

    def acquire_user_to_speak(self):
        self.utter("您在说话吗？请大声一点。")

    # END Behavior definitions

    def run(self):
        self.perform_welcoming()
        self.welcomed()
        while self.voice_detected():
            self.pointed_at_face()
            self.max_time_reached()
            pass
        self.perform_goodbye()
