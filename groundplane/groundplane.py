from landshark.controllers import pywemo_controller, camera_controller

class landshark(pywemo_controller, camera_controller):
    def state(self):
        return {}

    def __repr__(self):
        return json.dumps(self.definition, self.state)

