import pyttsx3
# from queue import Queue, Empty
from multiprocessing import Process, Queue
import logging
from robotic_arm.output.voice import tts_subprocess

logger = logging.getLogger(__name__)
engine = pyttsx3.init()
async_queue = Queue()


def load():
    async_engine_init()


def async_engine_init():
    process = Process(target=tts_subprocess.run, name="async-tts-process", daemon=True, args=(async_queue,))
    # thread = threading.Thread(target=async_engine_loop, name="tts")
    # thread.start()
    process.start()
    logger.info("Subprocess async-tts-process started!")
    utter_async("异步语音合成子进程初始化成功")


def async_engine_loop():
    # while True:
    #     text = async_queue.get(block=True)
    #     async_engine.say(text)
    pass
    # async_queue.task_done()


def utter(text: str):
    engine.say(text)
    engine.runAndWait()
    # async_queue.put(text)
    # async_queue.join()


def utter_async(text: str):
    # async_queue.put(text)
    # thread = threading.Thread(target=utter, args=(text,))
    # async_engine.say(text)
    # thread.start()
    async_queue.put(text)
