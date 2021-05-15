import logging
from queue import Empty
from time import sleep

import cv2
from transitions import Machine

from robotic_arm.input.camera import get_raw_frame
from robotic_arm.output import utter, utter_async
from robotic_arm.recognition import FaceRecognitionService, VoiceRecognitionService, HandsRecognitionService
from robotic_arm.utils import get_center_point, is_point_at_camera_center
from robotic_arm.motion.base import MotionBase


class RoboticArm(Machine):
    states = ['welcoming', 'voice_detecting', 'face_detecting', 'hand_tracking']

    def __init__(self,
                 face_service: FaceRecognitionService,
                 voice_service: VoiceRecognitionService,
                 hands_service: HandsRecognitionService,
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

        self.motion = motion_impl
        self.display = display_service

        self.logger = logging.getLogger(__name__)

    # BEGIN Voice command handlers

    # Handler Signature should be f: self -> shouldExitCommandLoop: bool

    def voice_command_hello_handler(self) -> bool:
        self.logger.info("Hello! From handler!")
        utter_async("我好得很!")
        return False

    def voice_command_exit_handler(self) -> bool:
        self.logger.info("Exit! From handler!")
        utter("即将退出")
        return True

    def hash_negative_812530379159490365_handler(self) -> bool:
        self.logger.info(f"我十分同意你的观点!")
        utter("我十分同意你的观点!")
        return False

    def hash_7951174358884070940_handler(self) -> bool:
        utter("很多人都以为我疯啦!")
        return False

    # routes
    voice_command_handlers = {
        "Hello": voice_command_hello_handler,
        "Exit": voice_command_exit_handler,
        "-812530379159490365": hash_negative_812530379159490365_handler,
        "7951174358884070940": hash_7951174358884070940_handler
    }

    def execute_voice_command(self, cmd: str) -> bool:
        self.logger.info(f"Executing voice command : {cmd}.")
        return self.voice_command_handlers[cmd](self)

    # END Voice command handlers

    # BEGIN Behavior definitions

    def perform_welcoming(self):
        print("Welcoming!")
        utter("你好呀? 你好吗?")
        sleep(0.1)
        utter_async("是不是同时听到了两条消息")
        for i in range(1):
            utter("同步语音消息输出测试")
            utter_async("异步语音消息输出测试")
        print("End Welcoming")

    def perform_goodbye(self):
        print("Welcoming!")
        sleep(5)

    def on_enter_voice_detecting(self):
        import random
        print("Voice detecting!")
        self.voice_service.wait_for_ready()
        self.voice_service.start_working()
        while True:
            try:
                cmd = self.voice_service.output_queue.get(block=True, timeout=10)
                if self.execute_voice_command(cmd):
                    break
            except Empty:
                self.acquire_user_to_speak()
                self.motion.set(0, random.random())
                self.motion.set(1, random.random())
                self.motion.set(2, random.random())

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
                utter_async("你去哪了,我正在找你呢?")
            else:
                utter_async("人都死光了吗?来个人让我瞧瞧")

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
                    utter_async("就你一个人?做好被枪毙的准备了吗?")
                    locked = True
                posx, posy = get_center_point(result[0].location_data)
                self.logger.debug(f"x:{posx},y:{posy}")
                if is_point_at_camera_center(posx, posy):
                    utter("你已经被枪毙了!")
                    self.logger.debug("You died!")
                    break
                else:
                    utter_async("请把头对准枪口")
            else:
                utter_async("好多人呀!我要随便挑一个枪毙!")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # self.face_service.stop_working()

    def on_enter_hand_tracking(self):
        import mediapipe as mp
        mp_drawing = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands
        print("Hand Tracking!")
        self.hands_service.wait_for_ready()
        # self.hands_service.start_working()
        while True:
            frame = get_raw_frame()
            if frame is None:
                continue
            try:
                # marks = None
                # while not self.hands_service.output_queue.empty():
                #    marks = self.hands_service.output_queue.get_nowait()
                marks = self.hands_service.output_queue.get_nowait()
                if not marks:
                    self.logger.info("Encountered empty marks!")
                    continue
                for mark in marks:
                    mp_drawing.draw_landmarks(
                        frame, mark, mp_hands.HAND_CONNECTIONS)
                cv2.imshow("Hands", frame)
            except Empty:
                pass
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # self.hands_service.stop_working()

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
