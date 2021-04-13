import os
from os import path
import hashlib
import json
import logging
from playsound import playsound

logger = logging.getLogger("mp3-composition")
sv_dict = dict()


def md5(text: str) -> str:
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
    dic = {text: md5(text) + '.wav' for text in texts}
    try:
        shutil.rmtree('assets')
    except:
        logger.warning("Failed to clear assets directory!")
    try:
        os.mkdir('assets')
    except:
        logger.warning("Failed to create assets directory!")
    for text in texts:
        e.save_to_file(text, path.join('assets', dic[text]))
        e.runAndWait()
        decorate_sound_file(2, path.join('assets', dic[text]))
        logger.info(f"Processed {text}.")
    with open("audio.json", "w", encoding='utf-8') as f:
        json.dump(dic, f)


def load():
    global sv_dict
    with open("audio.json", encoding='utf-8') as f:
        dic = json.load(f)
    sv_dict = {key: path.join('assets', dic[key])+'.wav' for key in dic}


def utter(text: str):
    logger.debug(f"Playing sound {sv_dict[text]}")
    playsound(sv_dict[text], block=True)


def utter_async(text: str):
    playsound(sv_dict[text], block=False)
