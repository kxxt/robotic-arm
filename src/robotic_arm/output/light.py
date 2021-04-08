from colour import Color


class Light:
    def __init__(self, pin: int):
        self.pin = pin

    def switch(self, c: Color, state: bool):
        pass

    def on(self, c: Color):
        pass

    def off(self):
        pass
