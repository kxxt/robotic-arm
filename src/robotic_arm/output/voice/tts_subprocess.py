from queue import Empty
import pyttsx3
from multiprocessing import Queue

engine = pyttsx3.init()


def run(input_queue: Queue):
    while True:
        try:
            text = input_queue.get_nowait()
            engine.say(text)
            engine.runAndWait()
        except Empty:
            pass
