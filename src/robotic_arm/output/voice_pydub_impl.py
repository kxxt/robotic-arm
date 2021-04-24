import logging
from pydub import AudioSegment
from pydub.playback import play
from robotic_arm.output.static_voice_preprocessor import get, get_dict, load as preload
import threading
from queue import Queue

logger = logging.getLogger("pydub")
voice_cache = dict()
q = Queue()


def utter(text: str):
    play(voice_cache[text])


def utter_async(text: str):
    q.put(text)


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
