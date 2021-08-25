""" Control code for anything connected to the GPIO bus """
import gpiozero
from groundplane.things import thing
from threading import Timer


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
    def __init__(self, SORT, DEVICE_TYPE, PIN, RETRACTION_TIMEOUT=30):
        super().__init__(SORT=SORT, DEVICE_TYPE="latch", PIN=PIN)
        self.unlock_timer = None
        self.RETRACTION_TIMEOUT = RETRACTION_TIMEOUT

    @property
    def extended(self):
        return self.gpo.value == 0

    def retract(self):
        return self.request_state({"state": "retracted"})

    def extend(self):
        return self.request_state({"state": "extended"})

    def state(self):
        state = super().state()
        state['state'] = 'retracted' if state['state'] == 1 else 'extended'
        return state

    def request_state(self, requested_state):
        state = requested_state.get("state", "extended").lower()
        assert state in ["extended", "retracted"], f"Latch state {state} not recognized"
        if state == "retracted":
            # A timed callback is created to extend the lock to prevent overheating
            self.unlock_timer = Timer(self.RETRACTION_TIMEOUT, self.extend)
            self.unlock_timer.start()
        elif self.unlock_timer is not None:
            self.unlock_timer.cancel()

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

