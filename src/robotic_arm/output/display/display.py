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

    def println(self, msg):
        self.queue.put(msg)

    def event_loop(self):
        from luma.core.render import canvas
        if self.mode == DisplayMode.CANVAS:
            while msg := self.queue.get(block=True):
                with canvas(self.device) as draw:
                    self.logger.info("Got Message!")
        elif self.mode == DisplayMode.TERMINAL:
            from luma.core.virtual import terminal
            font = ImageFont.truetype(path.join("res", "zpix.ttf"), 12, encoding='unic')
            term = terminal(self.device, font)
            term.println("OLED 显示服务初始化成功!")
            while msg := self.queue.get(block=True):
                term.println(msg)
        else:
            pass

    def process_draw_msg(self, msg):
        pass
