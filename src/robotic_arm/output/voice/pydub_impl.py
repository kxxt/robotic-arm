import logging
from pydub import AudioSegment
from pydub.playback import play
from robotic_arm.output.voice.static_voice_preprocessor import get, get_dict, load as preload
import threading
from queue import Queue, Full
from robotic_arm.config import ASYNC_VOICE_COMPOSITION_MAX_QUEUE_SIZE
from robotic_arm.output.voice.voice_base import voice_output_callback


logger = logging.getLogger("pydub")
voice_cache = dict()
q = Queue(maxsize=ASYNC_VOICE_COMPOSITION_MAX_QUEUE_SIZE)


def utter(text: str):
    voice_output_callback(text)
    play(voice_cache[text])


def utter_async(text: str):
    while True:
        try:
            q.put_nowait(text)
            break
        except Full:
            q.get()


def work():
    while True:
        utter(q.get(block=True))


thread = threading.Thread(target=work, name="pydub-queue", daemon=True)


def load():
    global voice_cache
    preload()
    # logger.debug(sv_dict)
    logger.info("Loading voice composition cache into memory...")
    voice_cache = {key: AudioSegment.from_wav(get(key)) for key in get_dict()}
    thread.start()
