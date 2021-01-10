import json
import pywemo
import cv2


class controller:
    def __init__(self, definition):
        # Gather required definition keys from all classes in instance's inheritance
        # Raise exception if required key not found
        required_keys = set([rkey for base in list(type(self).__bases__) + [type(self)]
                             for rkey in base.required_keys(self)])
        missing_rkeys = [key for key in required_keys if key not in definition]
        if missing_rkeys:
            raise KeyError(f"Missing needed keys in definition: {missing_rkeys}")
        self.definition = definition

        # Add definition keys as attributes to instance
        # Gather conflicting definition and existing attribute names, raise exception if >0
        cdef_keys = []
        for key, value in self.definition.items():
            try:
                getattr(self, key)
                cdef_keys.append(key)
            except AttributeError:
                pass
        if cdef_keys:
            raise Exception(f"Conflicting definition and method names: {cdef_keys}")
        for key, value in self.definition.items():
            setattr(self, key, value)

    def required_keys(self):
        """ Return the keys that must be in this controller's definition"""
        return []

    def __repr__(self):
        return json.dumps(self.definition)


class pywemo_controller(controller):
    def required_keys(self):
        return ['wemo_insights', 'wemo_outlets']

    @staticmethod
    def get_devices():
        return pywemo.discover_devices()

    @staticmethod
    def get_device(device_name):
        for device in get_devices():
            if device.name == device_name:
                return device
        raise Exception(f"Device {device_name} not found")


class camera_controller(controller):
    def required_keys(self):
        return ['cameras']

    @staticmethod
    def snapshot_cameras(cameras, filefmt="{cam}.png"):
        for cam in cameras:
            cv2.imwrite(filefmt.format(cam=cam), capture_camera(cam))


class gpio_controller(controller):
    def required_keys(self):
        return ['input_pins', 'output_pins']

    @staticmethod
    def toggle(pin_number):
        pass
    
    @staticmethod
    def call(self, new_state=None):
        """ If new_state is ~None, set state to new_state
            return state """
        pass

