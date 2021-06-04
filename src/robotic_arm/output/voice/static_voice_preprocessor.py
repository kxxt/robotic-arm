import logging
from os import path
import json
import os
from os.path import exists

from robotic_arm.config import VOICE_JSON_PATH, USE_PROCESSED_VOICE_FILE, NAME, STATIC_VOICE_PREPROCESSOR_MAX_ITERATIONS

logger = logging.getLogger("voice-preprocessor")
sv_dict = dict()


def md5(text: str) -> str:
    import hashlib
    h = hashlib.md5(text.encode())
    return h.hexdigest()


def decorate_sound_file(time, file):
    from os import system
    command = f'ffmpeg -y -f lavfi -t {time} -i anullsrc=channel_layout=stereo:sample_rate=22050 -i {file} -filter_complex "[0:a][1:a][0:a]concat=n=3:v=0:a=1" {file}.wav'
    logger.info(f"Executing: {command}")
    system(command)


def build_sound_files():
    import pyttsx3
    import shutil
    e = pyttsx3.init()
    with open("audio.list", encoding='utf-8') as f:
        texts = f.read().splitlines(keepends=False)
    magic_texts = {text for text in texts if "MAGICAL_CHINESE_NUMBER" in text}
    texts = [text.replace("NAME", NAME) for text in texts if text not in magic_texts]
    dic = {text: md5(text) + '.wav' for text in texts}
    mdic = {
        mtext.replace("MAGICAL_CHINESE_NUMBER", str(i)):
            md5(mtext.replace("MAGICAL_CHINESE_NUMBER", str(i))) + '.wav'
        for i in range(1, STATIC_VOICE_PREPROCESSOR_MAX_ITERATIONS)
        for mtext in magic_texts
    }
    try:
        os.mkdir('assets')
    except:
        logger.warning("Failed to create assets directory!")
    for text in texts:
        p = path.join('assets', dic[text])
        if exists(p):
            logger.info(f"Ignored {text} because it already exists!")
            continue
        e.save_to_file(text, p)
        e.runAndWait()
        decorate_sound_file(2, p)
        logger.info(f"Processed {text}.")
    import cn2an
    for text in mdic:
        p = path.join('assets', mdic[text])
        real_text = cn2an.transform(text, "an2cn")
        if exists(p):
            logger.info(f"Ignored {real_text} because it already exists!")
            continue
        e.save_to_file(real_text, p)
        e.runAndWait()
        decorate_sound_file(2, p)
        logger.info(f"Processed {real_text}.")
    dic.update(mdic)
    with open("audio.json", "w", encoding='utf-8') as f:
        json.dump(dic, f)


def load():
    global sv_dict
    logger.info("Loading Voice Composition JSON Data File...")
    with open(VOICE_JSON_PATH, encoding='utf-8') as f:
        dic = json.load(f)
    sv_dict = {key: path.join('assets', dic[key]) + ('.wav' if USE_PROCESSED_VOICE_FILE else '') for key in dic}
    # logger.debug(sv_dict)


def get(text: str) -> str:
    return sv_dict[text]


def get_dict():
    return sv_dict
