from threading import Thread
from PIL import ImageFont
from queue import Queue
import logging
from enum import Enum
from os import path


class DisplayMode(Enum):
    TERMINAL = 0
    CANVAS = 1


class Display:
    def __init__(self, device):
        self.logger = logging.getLogger("display")
        self.device = device
        self.queue = Queue()
        self.process = Thread(target=self.event_loop,
                              name="display", daemon=True)
        self.draw = None
        self.canvas = None
        # self.font = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf")
        self.logger.info("Display instantiated")
        self.mode = DisplayMode.TERMINAL

    def start(self):
        self.logger.info("Starting display service ...")
        # self.canvas = canvas(self.device)
        # self.draw = self.canvas.__enter__()
        # self.draw.rectangle(((0, 2), (40, 23)), 'white', None, 2)
        self.process.start()

    def event_loop(self):
        from luma.core.render import canvas
        font = ImageFont.truetype(r"C:\Windows\Fonts\SIMSUN.ttc", 16)
        with canvas(self.device) as draw:
            draw.text((0, 0), "Hello World！", fill="white", font=font)
        if self.mode == DisplayMode.CANVAS:
            while msg := self.queue.get(block=True):
                with canvas(self.device) as draw:
                    self.logger.info("Got Message!")
        elif self.mode == DisplayMode.TERMINAL:
            from luma.core.virtual import terminal
            font = ImageFont.truetype(path.join("res", "zpix.ttf"), 12, encoding='unic')
            term = terminal(self.device, font)
            import time
            term.println("启动成功")
            time.sleep(8)
            term.println("数据玄学与人工智障实验班")
            term.println("------------------")
            term.println("奇怪的机械臂")
            time.sleep(2)
            term.println("？？？？？")
            term.println()
            time.sleep(2)

            term.animate = False
            time.sleep(2)
            term.clear()

            term.println("Progress bar")
            term.println("------------")
            for mill in range(0, 10001, 25):
                term.puts("\rPercent: {0:0.1f} %".format(mill / 100.0))
                term.flush()

            time.sleep(2)
            term.clear()
            term.puts("Backspace test.")
            term.flush()
            time.sleep(2)
            for _ in range(17):
                term.backspace()
                time.sleep(0.2)
            time.sleep(2)
            term.clear()
            term.animate = True
            while msg := self.queue.get(block=True):
                term.println(msg)
        else:
            pass

    def process_draw_msg(self, msg):
        pass
