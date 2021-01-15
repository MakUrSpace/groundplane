import base64
from datetime import datetime
from traceback import format_exc
import cv2


from groundplane.things import thing


class camera(thing):
    def __init__(self, DEVICE_NUMBER):
        self.device_number = DEVICE_NUMBER
        self.cfg = {}

    def state(self):
        try:
            img = self.capture_camera(int(self.device_number)).decode()
        except:
            img = f"ERROR: Failed to capture image: {format_exc()}"
        return {"IMAGE": img, "CFG": self.cfg, "TIMESTAMP": datetime.utcnow().isoformat()}

    def request_state(self, requested_state):
        new_cfg = requested_state.get("CFG", self.cfg)
        self.cfg = new_cfg
        return True

    @staticmethod
    def capture_camera(cam_num):
        cam = cv2.VideoCapture(cam_num)
        retval, image = cam.read()
        cam.release()
        retval, buff = cv2.imencode('.jpg', image)
        b64jpg = base64.b64encode(buff)
        return b64jpg

