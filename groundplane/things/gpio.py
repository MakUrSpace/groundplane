""" Control code for anything connected to the GPIO bus """
import gpiozero
from groundplane.things import thing


class gpio(thing):
    def __init__(self, SORT, DEVICE_TYPE, PIN):
        super().__init__(SORT, DEVICE_TYPE)
        self.PIN = PIN
        self.gpo = None  # Child classes must override self.gpo in their own self.__init__

    def state(self):
        state = super().state()
        state['state'] = self.gpo.value
        return state


class out_pin(gpio):
    def __init__(self, SORT, DEVICE_TYPE, PIN):
        super().__init__(SORT, DEVICE_TYPE, PIN)
        self.gpo = gpiozero.DigitalOutputDevice(
            pin=self.PIN,
            initial_value=False)

    def request_state(self, requested_state):
        on_state = int(requested_state.get("state", None))
        assert on_state in [1, 0]
        if on_state == 1:
            self.gpo.on()
        else:
            self.gpo.off()
        return True


class latch(out_pin):
    def __init__(self, SORT, DEVICE_TYPE, PIN):
        super().__init__(SORT=SORT, DEVICE_TYPE="latch", PIN=PIN)

    @property
    def extended(self):
        return self.gpo.value == 0

    def retract(self):
        return super().request_state({"state": 1})

    def extend(self):
        return super().request_state({"state": 0})

    def state(self):
        state = super().state()
        state['state'] = 'retracted' if state['state'] == 1 else 'extended'
        return state

    def request_state(self, requested_state):
        state = requested_state.get("state", "extended")
        return super().request_state({"state": 0 if state == "extended" else 1})


class in_pin(gpio):
    def __init__(self, SORT, DEVICE_TYPE, PIN):
        super().__init__(SORT, DEVICE_TYPE, PIN)
        self.gpo = gpiozero.DigitalInputDevice(
            pin=self.PIN)

    def request_state(self, requested_state):
        raise Exception("Input Device cannot accept state request")


class mag_sensor(gpio):
    def __init__(self, SORT, DEVICE_TYPE, PIN):
        super().__init__(SORT=SORT, DEVICE_TYPE="mag_sensor", PIN=PIN)
        self.gpo = gpiozero.DigitalInputDevice(
            pin=self.PIN, pull_up=True)

    def request_state(self, requested_state):
        raise Exception("Input Device cannot accept state request")

    @property
    def field_present(self):
        return self.gpo.value == 1

