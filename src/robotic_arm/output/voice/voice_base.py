callbacks = set()


def register_voice_output_callback(callback):
    global callbacks
    callbacks.add(callback)


def voice_output_callback(msg: str):
    for callback in callbacks:
        callback(msg)
