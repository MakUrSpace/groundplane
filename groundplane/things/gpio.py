""" Control code for anything connected to the GPIO bus """
import json
import base64
from datetime import datetime
from traceback import format_exc
import pywemo
import cv2


import gpiozero
from groundplane.things import thing


class gpio(thing):
    def __init__(self, PIN):
        self.pin = PIN


class out_pin(gpio):
    def __init__(self, PIN):
        super().__init__()


class latch(gpio):
    def open(self):
        pass


class in_pin(gpio):
    def __init__(self, PIN):
        super().__init__(PIN=PIN)


class level_sensor(in_pin):
    pass


class mag_sensor(level_sensor):
    pass

