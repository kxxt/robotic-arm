from robotic_arm.config import VOICE_COMPOSE_SOLUTION

if VOICE_COMPOSE_SOLUTION == "mp3-files":
    from robotic_arm.output.voice_from_precomposed_mp3_impl import utter, utter_async, load
elif VOICE_COMPOSE_SOLUTION == "pyttsx3":
    from robotic_arm.output.voice_pyttsx3_impl import utter, utter_async, load
else:
    raise NotImplementedError("Must provide an implementation of voice composition!")
