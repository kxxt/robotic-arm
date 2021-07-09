try:
    import pigpio
except ImportError:
    import logging

    logger = logging.getLogger("GPIO")
    logger.error("Failed to import GPIO library: pigpio!")
    logger.error("Ignore this error if you are on other platforms, but all gpio functions won't work at all!")


    class FakeGPIO:
        def __getattr__(self, name):
            return self

        def __call__(self, *args, **kwargs):
            return


    pigpio = FakeGPIO()
pi = pigpio.pi()
