import logging
from pydub import AudioSegment
from pydub.playback import play
from robotic_arm.output.voice.static_voice_preprocessor import get, get_dict, load as preload
import threading
from queue import Queue, Full
from robotic_arm.config import ASYNC_VOICE_COMPOSITION_MAX_QUEUE_SIZE
from robotic_arm.output.voice.voice_base import voice_output_callback
from robotic_arm.output.voice.base import VoiceCompositionBase

class PydubVoiceComposition(VoiceCompositionBase):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("pydub")
        self.voice_cache = dict()
        self.q = Queue(maxsize=ASYNC_VOICE_COMPOSITION_MAX_QUEUE_SIZE)
        self.idle = threading.Event()
        self.thread = threading.Thread(target=self.work, name="pydub-queue", daemon=True)

    def utter(self, text: str):
        voice_output_callback(text)
        play(voice_cache[text])

    def utter_async(self, text: str):
        while True:
            try:
                self.q.put_nowait(text)
                break
            except Full:
                self.q.get()

    def utter_async_passive(self, text: str):
        if self.q.empty():
            self.utter_async(text)

    def clear_async_queue(self):
        with self.q.mutex:
            self.q.queue.clear()

    def wait_for_idle(self):
        self.idle.wait()

    def work(self):
        while True:
            self.idle.clear()
            self.utter(self.q.get(block=True))
            self.idle.set()

    def load(self):
        global voice_cache
        self.idle.set()
        preload()
        # logger.debug(sv_dict)
        self.logger.info("Loading voice composition cache into memory...")
        voice_cache = {key: AudioSegment.from_wav(get(key)) for key in get_dict()}
        self.thread.start()
