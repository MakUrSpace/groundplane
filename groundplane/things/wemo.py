from datetime import datetime
import pywemo

from groundplane.things import thing


def get_wemo_devices(force_scan=False):
    if not get_wemo_devices.devices or force_scan:
        get_wemo_devices.devices = pywemo.discover_devices()
    return get_wemo_devices.devices


get_wemo_devices.devices = []


class wemo(thing):
    def __init__(self, SORT, DEVICE_NAME):
        self.SORT = SORT
        self.device_name = DEVICE_NAME
        self.wemo = self.get_device(DEVICE_NAME)

    @staticmethod
    def get_device(device_name):
        for device in get_wemo_devices():
            if device.name == device_name:
                return device
        raise Exception(f"Device {device_name} not found")


class wemo_plug(wemo):
    def state(self):
        return {"state": self.wemo.get_state() == 1,
                "TIMESTAMP": datetime.utcnow().isoformat()}

    def request_state(self, requested_state):
        on_state = int(requested_state.get("state", None))
        assert on_state in [1, 0]
        self.wemo.set_state(on_state)
        return True

    def toggle(self):
        self.wemo.toggle()


class wemo_insight(wemo_plug):
    def get_insight_params(self):
        self.wemo.update_insight_params()
        return self.wemo.insight_params

    def state(self):
        insight_params = self.get_insight_params()
        insight_params['lastchange'] = insight_params['lastchange'].isoformat()
        return {**insight_params,
                "TIMESTAMP": datetime.utcnow().isoformat()}
