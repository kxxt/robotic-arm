import threading
from queue import Queue
import logging


class RecognitionServiceBase:
    def __init__(self, name='recognition', output_queue_size=0):
        self.thread = threading.Thread(target=self.work, name=name)
        self.thread.setDaemon(True)
        self.loaded = threading.Event()
        self.input_queue = Queue()
        self.output_queue = Queue(maxsize=output_queue_size)
        self.working = threading.Event()
        self.logger = logging.getLogger(__name__)

    def load(self):
        pass

    def run(self):
        self.thread.start()

    def wait_for_ready(self):
        if not self.loaded.isSet():
            self.loaded.wait()

    def real_work(self):
        pass

    def work(self):
        self.logger.info("Service loading!")
        self.load()
        self.loaded.set()
        self.logger.info("Service loaded!")
        while True:
            # self.logger.debug("Waiting for working...")
            self.working.wait()
            # self.logger.debug("Get working!")
            self.real_work()

    def start_working(self):
        self.working.set()
        self.logger.info("Now started working!")

    def stop_working(self):
        self.working.clear()
        self.logger.info("Now stopped working!")
