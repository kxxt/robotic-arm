import logging
from queue import Empty
import os

import cv2
import numpy as np
from transitions import Machine

from robotic_arm.config import NAME
from robotic_arm.input.camera import get_raw_frame
from robotic_arm.output import VoiceCompositionBase
from robotic_arm.recognition import FaceRecognitionService, VoiceRecognitionService, HandsRecognitionService
from robotic_arm.utils import get_center_point, is_point_at_camera_center
from robotic_arm.utils.judge import get_diff_vector_from_center
from robotic_arm.motion.base import MotionBase
from math import pi
from time import sleep


class RoboticArm(Machine):
    states = ['welcoming', 'voice_detecting', 'face_detecting', 'hand_tracking']

    def __init__(self,
                 face_service: FaceRecognitionService,
                 voice_service: VoiceRecognitionService,
                 hands_service: HandsRecognitionService,
                 voice_composition: VoiceCompositionBase,
                 motion_impl: MotionBase,
                 display_service,
                 light,
                 light_sensor):
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
        self.light = light
        self.light_sensor = light_sensor

        self.logger = logging.getLogger(__name__)

        self.p4 = None
        self.p2 = None
        self.reset_pose()

    def reset_pose(self):
        for i in range(1, 5):
            if i != 3:
                self.motion.set(i, 0, 500)
        self.motion.set(3, pi / 12, 500)
        self.motion.set(5, -pi / 24, 500)

    def welcome_pose(self):
        from math import pi
        from time import sleep
        sleep(3)
        self.motion.set(3, -pi / 3, 1000)
        self.utter_async(f"您好，{NAME}为您服务。")
        sleep(4)
        self.motion.set(3, pi / 12, 1000)

    def move_up_down(self, dir):
        """
        move up or down.
        :param dir: up -> true, down -> false
        :return:
        """
        dir = 1 if dir else -1
        # p2 = self.motion.get(2)
        # p4 = self.motion.get(4)
        delta = pi / 90
        self.p2 += delta * dir
        self.p4 -= delta * dir
        self.motion.set(2, self.p2, 200)
        self.motion.set(4, self.p4, 200)
        sleep(1)

    def move_right_left(self, dir):
        dir = 1 if dir else -1
        delta = pi / 90
        cur = self.motion.get(1)
        self.motion.set(1, cur + delta * dir)

    def face_recogn_judge_move_vertical_direction(self, data):
        vec = get_diff_vector_from_center(data)
        return vec[1] < 0

    def face_recogn_judge_move_horizontal_direction(self, data):
        vec = get_diff_vector_from_center(data)
        return vec[0] < 0

    def face_recognition_init_pose(self):
        from time import sleep
        from math import pi
        self.reset_pose()
        sleep(1)
        ang = pi / 4
        self.p2 = -ang
        self.p4 = 3 * pi / 8
        self.motion.set(2, self.p2, 1000)
        self.motion.set(4, self.p4, 1000)
        self.motion.set(3, pi / 12, 1000)
        # self.motion.set(1, -pi / 2, 1000)
        sleep(2)

    def hand_tracking_init_pose(self):
        from time import sleep
        from math import pi
        sleep(1)
        ang = pi / 4
        self.p2 = -ang
        self.p4 = pi / 4
        self.motion.set(2, self.p2, 1000)
        self.motion.set(4, self.p4, 1000)
        self.motion.set(3, pi / 12, 1000)
        self.motion.set(1, 0, 1000)
        # self.motion.set(1, -pi / 2, 1000)
        sleep(2)

    def x_walk1(self):
        from math import pi
        self.motion.set(1, -pi / 4, 1000)
        self.motion.set(2, 3 * pi / 4, 2000)
        self.motion.set(3, pi / 4, 1000)
        self.motion.set(4, pi / 2)

    # BEGIN Voice command handlers

    # Handler Signature should be f: self -> shouldExitCommandLoop: bool

    def voice_command_hello_handler(self) -> bool:
        from math import pi
        import time
        self.logger.info("Hello! From handler!")
        self.utter_async("我好得很!")
        # self.motion.set(3, pi / 2, 2000)
        # time.sleep(2.1)
        # self.motion.set(3, -pi / 2, 3000)
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
        self.light.start_flicker()
        self.voice_composition.clear_async_queue()
        # self.voice_composition.wait_for_idle()
        # self.light.start_flicker()
        self.welcome_pose()
        self.utter(f"程序加载完成，试试对我说{NAME}{NAME}。")

    def perform_goodbye(self):
        self.utter("感谢您的使用，程序即将退出。")
        self.display.device.cleanup()
        self.reset_pose()
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
        self.light.stop_flicker()
        self.light.off()
        import mediapipe as mp
        drawing = mp.solutions.drawing_utils
        self.face_recognition_init_pose()
        self.utter("正在检测环境亮度")
        li = None
        li = self.light_sensor.read()
        if not li:
            self.utter("好像有点暗，已为您开灯。")
            self.light.on()
        print("face detecting")
        self.face_service.wait_for_ready()
        print("Face detector ready!")
        # self.face_service.start_working()
        locked = False
        miss_cnt = 0

        def act_on_no_body(found, miss_cnt):
            miss_cnt += 1
            if miss_cnt > 5:
                miss_cnt = 0
                if found:
                    self.utter_async_passive("你去哪了,我正在找你呢?")
                else:
                    self.utter_async_passive("人都去哪了？怎么突然没人了？")
            return miss_cnt

        while True:
            result = self.face_service.recognize_sync()
            if result is None:
                miss_cnt = act_on_no_body(locked, miss_cnt)
                continue
            image = None
            while image is None:
                image = get_raw_frame()
            for detection in result:
                drawing.draw_detection(image, detection)
            # cv2.imshow("Face", image)
            le = len(result)
            if le == 0:
                miss_cnt = act_on_no_body(locked, miss_cnt)
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
                    self.move_up_down(self.face_recogn_judge_move_vertical_direction(result[0].location_data))
                    self.move_right_left(self.face_recogn_judge_move_horizontal_direction(result[0].location_data))
                    # nq = self.motion.physics._move(result[0].location_data)
                    # self.motion.set_all(nq.q)
            else:
                self.utter_async(f"已经在{le}个人中圈定了一个人")
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #
        # self.face_service.stop_working()

    def move_hand(self, dirs):
        self.move_hand_x(dirs[0])
        self.move_hand_y(dirs[0])

    def move_hand_x(self, dir):
        dir = 1 if dir else -1
        delta = pi / 90
        cur = self.motion.get(1)
        self.motion.set(1, cur + delta * dir)

    def move_hand_y(self, dir):
        dir = 1 if dir else -1
        delta = pi / 90
        self.p2 -= delta * dir
        self.p4 += delta * dir
        self.motion.set(2, self.p2, 200)
        self.motion.set(4, self.p4, 200)
        sleep(1)

    def ikine_get_position(self, diff, dis=1):
        v = self.motion.physics.camera_to_world(diff, dis)
        q = self.motion.physics.ikine_min(v).q

    @staticmethod
    def hand_position_diff_vector(vbefore, vafter):
        diff = np.array(vafter) - np.array(vbefore)
        return diff / np.linalg.norm(diff)

    def judge_hand_direction(self, diff):
        return (diff[0] > 0, diff[1] > 0)

    def average_hand_position(self, data):
        sumx = 0
        sumy = 0
        for landmark in data.landmark:
            sumx += landmark.x
            sumy += landmark.y
        return sumx / len(data.landmark), sumy / len(data.landmark)

    def on_enter_hand_tracking(self):
        self.light.off()
        self.hand_tracking_init_pose()
        self.hands_service.wait_for_ready()
        self.logger.info("Hand tracking ready.")
        # self.hands_service.start_working()
        self.logger.info("Hand tracking running!")
        executed = False
        old_pos = None
        while True:
            try:
                # marks = None
                # while not self.hands_service.output_queue.empty():
                #    marks = self.hands_service.output_queue.get_nowait()
                marks = self.hands_service.recognize_sync()
                if not marks:
                    self.logger.info("Encountered empty marks!")
                    continue
                else:
                    apos = self.average_hand_position(marks[0])
                    if old_pos is not None:
                        v = self.hand_position_diff_vector(old_pos, apos)
                        dirs = self.judge_hand_direction(v)
                        self.move_hand(dirs)
                    old_pos = apos
                    # mp_drawing.draw_landmarks(frame, mark, mp_hands.HAND_CONNECTIONS)

                if not executed:
                    executed = True
                    mark = marks[0]
                self.logger.info("Running!!!")
                # cv2.imshow("Hands", frame)
            except Empty:
                pass
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break
        self.hands_service.stop_working()
        self.utter("手势追踪时间已到，正在返回语音识别状态!")
        return

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
