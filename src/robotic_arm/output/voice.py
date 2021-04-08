import pyttsx3

engine = pyttsx3.init()


def utter(text: str):
    engine.say(text)
    engine.runAndWait()
