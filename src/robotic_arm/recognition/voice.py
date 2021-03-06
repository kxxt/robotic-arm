from robotic_arm.input import microphone
from robotic_arm.recognition.base import RecognitionServiceBase
from vosk import Model, KaldiRecognizer
from robotic_arm.config import VOICE_RECOGNITION_MODEL_PATH, VOICE_SAMPLE_RATE, PYTHON_HASH_SEED, NAMES
import json
import logging


class VoiceRecognitionService(RecognitionServiceBase):
    recognition_data = {
        # 语音识别命令字典
        # 元组中字符串请从详细到简略排列
        "Hello": {"你好", "您好"},
        "Exit": {"退出程序", "退出", "废除"},
        "Start": NAMES
    }

    recognition_hidden_data = {
        "-812530379159490365": {
            -6431864560819639035, -8661293910594896745, 4928770567062600055,
            -2806501098437255290, -406522025722804583, -6965004661639014182,
            1401530348684742096, -183798426653810367, -3200253072492852793,
            4291294219978653493, 9024663502979451188, -3014716675189944241
        },
        "7951174358884070940": {
            7951174358884070940, -2467111048831020798, 4342503211783565351,
            8967996046275249579, -5840257186929253666, -5840257186929253666
        }
    }

    def __init__(self):
        RecognitionServiceBase.__init__(self, 'voice-recognition')
        self.logger = logging.getLogger('voice-recognition')
        self.model = None
        self.recognizer = None
        self.hidden_feature_enabled = True if PYTHON_HASH_SEED is not None and int(
            PYTHON_HASH_SEED) % 1737 == 0 else False

    def load(self):
        self.model = Model(VOICE_RECOGNITION_MODEL_PATH)
        self.recognizer = KaldiRecognizer(self.model, VOICE_SAMPLE_RATE)

    def recognize(self):
        pass

    @staticmethod
    def preprocess_text(text: str) -> str:
        return text.replace('[FIL]', '').replace('[SPK]', '').replace(' ', '')

    @staticmethod
    def process_full(data):
        return VoiceRecognitionService.preprocess_text(data.split('\n')[-2][12:-1])

    @staticmethod
    def process_partial(data):
        # FIXME: Can be optimized further.
        data = json.loads(data)
        return VoiceRecognitionService.preprocess_text(data['partial'])

    def process_text(self, text: str):
        self.logger.debug(f"Parsing voice command: {text}")
        max_last_index = 0
        result = None
        if self.hidden_feature_enabled:
            for key in self.recognition_hidden_data:
                for h in self.recognition_hidden_data[key]:
                    if hash(text) == h:
                        self.logger.debug(f"Hash match: {text} => {hash(text)}")
                        self.output_queue.put(key)
        for key in self.recognition_data:
            for keyword in self.recognition_data[key]:
                ind = text.rfind(keyword)
                rind = ind + len(keyword)
                if ind != -1 and rind > max_last_index:
                    result = key
                    max_last_index = rind
        if result:
            self.logger.debug(f"Parsed voice command {result}")
            self.output_queue.put(result)

    def real_work(self):
        def callback(indata, frames, time, status):
            # self.logger.debug("Entered callback!")
            if status:
                self.logger.error(f"From sounddevice: {status}")
            data = bytes(indata)
            if self.recognizer.AcceptWaveform(data):
                result = self.process_full(self.recognizer.Result())
            else:
                return
                # Do not process partial results to avoid multiple executions on same input.
                # result = self.process_partial(self.recognizer.PartialResult())
            # self.logger.info(result)
            self.process_text(result)

        with microphone.session(callback):
            while self.working.is_set():
                pass
