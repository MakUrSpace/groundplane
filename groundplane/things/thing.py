from datetime import datetime


class thing:
    def state(self):
        return {"TIMESTAMP": datetime.utcnow().isoformat()}

    def request_state(self, requested_state):
        return True
