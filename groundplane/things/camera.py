import base64
from datetime import datetime
from traceback import format_exc
import cv2


from groundplane.things import thing


def capture_camera(cam_num):
    cam = cv2.VideoCapture(cam_num)
    retval, image = cam.read()
    cam.release()
    retval, buff = cv2.imencode('.jpg', image)
    b64jpg = base64.b64encode(buff)
    return b64jpg


def identify_cameras(device_numbers=list(range(20))):
    functional = []
    for dn in device_numbers:
        try:
            img = capture_camera(dn)
            functional.append(dn)
        except Exception:
            continue
    return functional


class camera(thing):
    def __init__(self, SORT, DEVICE_TYPE, DEVICE_NUMBER):
        super().__init__(SORT, DEVICE_TYPE)
        self.DEVICE_NUMBER = DEVICE_NUMBER
        self.cfg = {}

    def state(self):
        try:
            img = self.capture_camera(int(self.DEVICE_NUMBER)).decode()
        except Exception:
            img = f"ERROR: Failed to capture image: {format_exc()}"
        return {"IMAGE": img, "CFG": self.cfg, "TIMESTAMP": datetime.utcnow().isoformat()}

    def request_state(self, requested_state):
        new_cfg = requested_state.get("CFG", self.cfg)
        self.cfg = new_cfg
        return True


class dyn_camera(thing):
    def __init__(self, SORT, DEVICE_TYPE, NUM_CAMERA, SCAN_CAMERAS=10):
        super().__init__(SORT, DEVICE_TYPE)
        self.NUM_CAMERA = NUM_CAMERA
        self.camera_numbers = identify_cameras(list(range(SCAN_CAMERAS)))
        if len(self.camera_numbers) < NUM_CAMERA:
            raise Exception(f"Unable to locate {NUM_CAMERA} cameras")

    def state(self):
        state = {}
        for dn in self.camera_numbers:
            try:
                img = capture_camera(dn)
                state[str(dn)] = img
            except Exception:
                img = f"ERROR: Failed to capture image: {format_exc()}"
        state['TIMESTAMP'] = datetime.utcnow().isoformat()
        return state

