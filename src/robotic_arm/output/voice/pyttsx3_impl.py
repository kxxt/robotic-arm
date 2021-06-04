import pyttsx3
# from queue import Queue, Empty
from multiprocessing import Process, Queue
import logging
from robotic_arm.output.voice import tts_subprocess
from robotic_arm.output.voice.base import VoiceCompositionBase


class Pyttsx3VoiceComposition(VoiceCompositionBase):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.engine = pyttsx3.init()
        self.async_queue = Queue()

    def load(self):
        self.async_engine_init()

    def async_engine_init(self):
        process = Process(target=tts_subprocess.run, name="async-tts-process", daemon=True, args=(self.async_queue,))
        # thread = threading.Thread(target=async_engine_loop, name="tts")
        # thread.start()
        process.start()
        self.logger.info("Subprocess async-tts-process started!")
        self.utter_async("异步语音合成子进程初始化成功")

    def async_engine_loop(self):
        # while True:
        #     text = async_queue.get(block=True)
        #     async_engine.say(text)
        pass
        # async_queue.task_done()

    def utter(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()
        # async_queue.put(text)
        # async_queue.join()

    def utter_async(self, text: str):
        # async_queue.put(text)
        # thread = threading.Thread(target=utter, args=(text,))
        # async_engine.say(text)
        # thread.start()
        self.async_queue.put(text)

    def utter_async_passive(self, text: str):
        if self.async_queue.empty():
            self.utter_async(text)

    def clear_async_queue(self):
        with self.async_queue.mutex:
            self.async_queue.queue.clear()
