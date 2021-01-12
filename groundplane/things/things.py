import json
import base64
from datetime import datetime
import pywemo
import cv2


class thing:
    def state(self):
        return {"TIMESTAMP": datetime.utcnow().isoformat()}


def get_wemo_devices(force_scan=False):
    if not get_wemo_devices.devices or force_scan:
        get_wemo_devices.devices = pywemo.discover_devices()
    return get_wemo_devices.devices
get_wemo_devices.devices = []


class wemo(thing):
    def __init__(self, DEVICE_NAME):
        self.device_name = DEVICE_NAME
        self.wemo = self.get_device(DEVICE_NAME)

    @staticmethod
    def get_device(device_name):
        for device in get_wemo_devices():
            if device.name == device_name:
                return device
        raise Exception(f"Device {device_name} not found")


class wemo_plug(wemo):
    def toggle(self):
        pass


class wemo_insight(wemo_plug):
    def get_insight_params(self):
        self.wemo.update_insight_params()
        return self.wemo.insight_params
    
    def state(self):
        return {**self.get_insight_params(),
                "TIMESTAMP": datetime.utcnow().isoformat()}


class camera(thing):
    def __init__(self, DEVICE_NUMBER):
        self.device_number = DEVICE_NUMBER

    def state(self):
        return {"IMAGE": "not implemented",  # self.capture_camera(self.device_number),
                "TIMESTAMP": datetime.utcnow().isoformat()}

    @staticmethod
    def capture_camera(cam_num):
        cam = cv2.VideoCapture(cam_num)
        retval, image = cam.read()
        cam.release()
        retval, buff = cv2.imencode('.jpg', image)
        b64jpg = base64.b64encode(buff)
        return b64jpg


class gpio(thing):
    def __init__(self, PIN):
        self.pin = PIN

    @staticmethod
    def toggle(pin_number):
        pass


class latch(gpio):
    def open(self):
        pass


class mag_sensor(gpio):
    pass

