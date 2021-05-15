from queue import Empty
import pyttsx3
from multiprocessing import Queue

engine = pyttsx3.init()


def run(input_queue: Queue):
    while text := input_queue.get(block=True):
        engine.say(text)
        engine.runAndWait()
