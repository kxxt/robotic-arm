from robotic_arm.config import VOICE_COMPOSE_SOLUTION

if VOICE_COMPOSE_SOLUTION == "playsound":
    from robotic_arm.output.voice_playsound_impl import utter, utter_async, load as load_voice_composition_service
elif VOICE_COMPOSE_SOLUTION == "pydub":
    from robotic_arm.output.voice_pydub_impl import utter, utter_async, load as load_voice_composition_service
elif VOICE_COMPOSE_SOLUTION == "pyttsx3":
    from robotic_arm.output.voice_pyttsx3_impl import utter, utter_async, load as load_voice_composition_service
else:
    raise NotImplementedError("Must provide an implementation of voice composition!")
