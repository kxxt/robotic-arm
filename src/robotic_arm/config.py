# Configurations for robotic-arm
from os import path, environ
import sounddevice as sd
import logging

NAME = '机器人'

ARM_LENGTHS = []
SERVO_PINS = []
LIGHT_PIN = environ.get('LIGHT_PIN') or 14

VOICE_RECOGNITION_MODEL_PATH = environ.get('VOICE_RECOGNITION_MODEL_PATH') \
                               or path.join('..', "models", "voice_recognition")

VOICE_DEVICE = environ.get('VOICE_DEVICE')

VOICE_SAMPLE_RATE = environ.get('VOICE_SAMPLE_RATE') \
                    or int(sd.query_devices(VOICE_DEVICE, 'input')['default_samplerate'])

VOICE_CHANNELS = environ.get('VOICE_CHANNELS') or 1

VOICE_BLOCKSIZE = environ.get('VOICE_BLOCKSIZE') or 8000

LOGGING_LEVEL = logging.DEBUG

CAMERA_ID = environ.get('CAMERA_ID') or 0

# available solutions are mp3-files, pyttsx3
VOICE_COMPOSE_SOLUTION = environ.get('VOICE_COMPOSE_SOLUTION') or "mp3-files"
