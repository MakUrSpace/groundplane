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
    def __init__(self, **kwargs):
        kwargs = {key.lower(): value for key, value in kwargs.items()}
        if 'pin' not in kwargs:
            raise Exception("GPIO pin definition required")
        self.kwargs = kwargs
        self.gpo = None

    def state(self):
        state = super().state()
        state['state'] = self.gpo.value
        return state

    @property
    def pin(self):
        return self.kwargs['pin']


class out_pin(gpio):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gpo = gpiozero.DigitalOutputDevice(**self.kwargs)

    def request_state(self, requested_state):
        on_state = int(requested_state.get("state", None))
        assert on_state in [1, 0]
        if on_state == 1:
            self.gpo.on()
        else:
            self.gpo.off()
        return True


class latch(out_pin):
    @property
    def closed(self):
        return self.gpo.value == 0
    
    def open(self):
        return super().request_state({"state": 1})

    def close(self):
        return super().request_state({"state": 0})

    def state(self):
        state = super().state()
        state['state'] = 'retracted' if state['state'] == 1 else 'extended'
        return state

    def request_state(self, requested_state):
        state = requested_state.get("state", "extended")
        return super().request_state({"state": 0 if state == "extended" else 1})
        

class in_pin(gpio):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gpo = gpiozero.DigitalInputDevice(**self.kwargs)

    def request_state(self, requested_state):
       return True 


class mag_sensor(in_pin):
    pass

