from robotic_arm.config import VOICE_COMPOSE_SOLUTION
from robotic_arm.output.voice.voice_base import register_voice_output_callback

if VOICE_COMPOSE_SOLUTION == "playsound":
    from robotic_arm.output.voice.playsound_impl import utter, utter_async, load as load_voice_composition_service
elif VOICE_COMPOSE_SOLUTION == "pydub":
    from robotic_arm.output.voice.pydub_impl import utter, utter_async, load as load_voice_composition_service
elif VOICE_COMPOSE_SOLUTION == "pyttsx3":
    from robotic_arm.output.voice.pyttsx3_impl import utter, utter_async, load as load_voice_composition_service
else:
    raise NotImplementedError("Must provide an implementation of voice composition!")
