from robotic_arm.config import *
import sounddevice as sd


def session(callback):
    return sd.RawInputStream(
        samplerate=VOICE_SAMPLE_RATE,
        blocksize=VOICE_BLOCKSIZE,
        device=VOICE_DEVICE,
        channels=VOICE_CHANNELS,
        dtype='int16',
        callback=callback
    )
