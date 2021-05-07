# Configurations for robotic-arm
from os import path, environ
import sounddevice as sd
import logging

# Basic profile data
NAME = '机器人'

# Hardware configurations
ARM_LENGTHS = []
SERVO_PINS = []

# Electronic configurations
LIGHT_PIN = environ.get('LIGHT_PIN') or 14

# Application configurations
LOGGING_LEVEL = logging.DEBUG

# Camera configurations
CAMERA_ID = environ.get('CAMERA_ID') or 0

# Voice composition configurations

# available solutions are pydub, playsound, pyttsx3
VOICE_COMPOSE_SOLUTION = environ.get('VOICE_COMPOSE_SOLUTION') or "pydub"
VOICE_JSON_PATH = environ.get('VOICE_JSON_PATH') or "audio.json"
USE_PROCESSED_VOICE_FILE = environ.get('USE_PROCESSED_VOICE_FILE') or False
ASYNC_VOICE_COMPOSITION_MAX_QUEUE_SIZE = environ.get('ASYNC_VOICE_COMPOSITION_MAX_QUEUE_SIZE') or 3

# face recognition configurations

# available solutions are face_recognition, mediapipe
FACE_RECOGNITION_SOLUTION = environ.get('FACE_RECOGNITION_SOLUTION') or "mediapipe"

# Mediapipe face_detection configurations.
MEDIAPIPE_FACE_DETECTION_MIN_CONFIDENCE = environ.get('MEDIAPIPE_FACE_DETECTION_MIN_CONFIDENCE') or 0.5

# hand tracking configurations
HANDS_MIN_DETECTION_CONFIDENCE = environ.get('HANDS_MIN_DETECTION_CONFIDENCE') or 0.5
HANDS_MIN_TRACKING_CONFIDENCE = environ.get('HANDS_MIN_TRACKING_CONFIDENCE') or 0.5

# Voice recognition configurations
VOICE_RECOGNITION_MODEL_PATH = environ.get('VOICE_RECOGNITION_MODEL_PATH') \
                               or path.join("models", "voice_recognition")
VOICE_DEVICE = environ.get('VOICE_DEVICE')
VOICE_SAMPLE_RATE = environ.get('VOICE_SAMPLE_RATE') \
                    or int(sd.query_devices(VOICE_DEVICE, 'input')['default_samplerate'])
VOICE_CHANNELS = environ.get('VOICE_CHANNELS') or 1
VOICE_BLOCKSIZE = environ.get('VOICE_BLOCKSIZE') or 8000

# Judgement configurations
CAMERA_CENTER_JUDGEMENT_OFFSET = environ.get('CAMERA_CENTER_JUDGEMENT_OFFSET') or 0.09
CAMERA_CENTER_AREA_JUDGEMENT_RATIO = environ.get('CAMERA_CENTER_AREA_JUDGEMENT_RATIO') or 0.3

# Lazy configurations
__load_real_services = environ.get('LOAD_REAL_SERVICES')
LOAD_REAL_SERVICES = True if __load_real_services is None else __load_real_services.lower() != "false"
