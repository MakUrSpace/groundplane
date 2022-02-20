from datetime import datetime
import kasa
import asyncio

from groundplane.things import thing


def get_kasa_devices(force_scan=False):
    if not get_kasa_devices.devices or force_scan:
        get_kasa_devices.devices = asyncio.run(kasa.Discover.discover())
    return get_kasa_devices.devices


get_kasa_devices.devices = []


class kasa_device(thing):
    def __init__(self, SORT, DEVICE_TYPE, DEVICE_ADDRESS, KASA_CLASS):
        super().__init__(SORT, DEVICE_TYPE)
        self.DEVICE_ADDRESS = DEVICE_ADDRESS
        assert KASA_CLASS in [c.__name__ for c in kasa.SmartDevice.__subclasses__()]
        self.KASA_CLASS = KASA_CLASS
        kasa_class = getattr(kasa, KASA_CLASS)
        self.kasa = kasa_class(DEVICE_ADDRESS)
        self.update()
        self.child_map = {c.alias: c for c in self.kasa.children}

    @staticmethod
    def get_device(device_name):
        for device in get_kasa_devices():
            if device.alias == device_name:
                return device
        raise Exception(f"Device {device_name} not found")

    def update(self):
        try:
            asyncio.get_running_loop().create_task(self.kasa.update())
        except RuntimeError:
            asyncio.run(self.kasa.update())


class kasa_strip(kasa_device):
    def __init__(self, SORT, DEVICE_TYPE, DEVICE_ADDRESS):
        super().__init__(SORT, DEVICE_TYPE, DEVICE_ADDRESS, KASA_CLASS="SmartStrip")

    def state(self):
        retries = 2
        while retries > 0:
            try:
                self.update()
                return {"state": {c.alias: c.is_on for c in self.kasa.children},
                        "TIMESTAMP": datetime.utcnow().isoformat()}
            except RuntimeError:
                retries -= 1
                if retries == 0:
                    raise

    def request_state(self, requested_state):
        state_requests = []
        for child, state in requested_state.items():
            cdevice = self.child_map[child]
            method = 'turn_on' if bool(state) else 'turn_off'
            state_requests.append(getattr(cdevice, method)())

        async def request_children():
            await asyncio.gather(*state_requests)
        try:
            asyncio.run(request_children())
        except Exception:
            cState = self.state()
            for key, value in requested_state.items():
                assert value == cState['state'][key], f"Failed to set kasa_strip.{key} to {value}"
        return True
